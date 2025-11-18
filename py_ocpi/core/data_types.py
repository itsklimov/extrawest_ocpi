"""
OCPI data types based on https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc
"""

from datetime import datetime, timezone
from typing import Any, Type
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

from .config import settings


class StringBase(str):
    """
    Case sensitive String. Only printable UTF-8 allowed.
    (Non-printable characters like:
    Carriage returns, Tabs, Line breaks, etc are not allowed)
    """

    max_length: int

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "StringBase":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: str) -> "StringBase":
        if not isinstance(v, str):
            raise TypeError(f"excpected string but received {type(v)}")
        try:
            v.encode("UTF-8")
        except UnicodeError as e:
            raise ValueError("invalid string format") from e
        if len(v) > cls.max_length:
            raise ValueError(
                f"string length must be lower or equal to {cls.max_length}"
            )
        return cls(v)

    def __repr__(self):
        return f"String({super().__repr__()})"


class String:
    def __new__(cls, max_length: int = 255) -> Type[str]:  # type: ignore
        return type("String", (StringBase,), {"max_length": max_length})


class CiStringBase(str):
    """
    Case Insensitive String. Only printable ASCII allowed.
    (Non-printable characters like:
    Carriage returns, Tabs, Line breaks, etc are not allowed)
    """

    max_length: int

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "CiStringBase":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: str) -> "CiStringBase":
        if not isinstance(v, str):
            raise TypeError(f"excpected string but received {type(v)}")
        if not v.isascii():
            raise ValueError("invalid cistring format")
        if len(v) > cls.max_length:
            raise ValueError(
                f"cistring length must be lower or equal to {cls.max_length}"
            )

        if settings.CI_STRING_LOWERCASE_PREFERENCE:
            return cls(v.lower())

        return cls(v.upper())

    def __repr__(self):
        return f"CiString({super().__repr__()})"


class CiString:
    def __new__(cls, max_length: int = 255) -> type:  # type: ignore
        return type("CiString", (CiStringBase,), {"max_length": max_length})


class URL(str):
    """
    An URL a String(255) type following the
    http://www.w3.org/Addressing/URL/uri-spec.html
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "URL":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: str) -> "URL":
        # Use StringBase validation directly
        StringType = String(255)
        if not isinstance(v, str):
            raise TypeError(f"excpected string but received {type(v)}")
        try:
            v.encode("UTF-8")
        except UnicodeError as e:
            raise ValueError("invalid string format") from e
        if len(v) > 255:
            raise ValueError("url length must be lower or equal to 255")
        return cls(v)

    def __repr__(self):
        return f"URL({super().__repr__()})"


class DateTime(str):
    """
    All timestamps are formatted as string(25) following RFC 3339,
    with some additional limitations.
    All timestamps SHALL be in UTC.
    The absence of the timezone designator implies a UTC timestamp.
    Fractional seconds MAY be used.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "DateTime":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: str) -> "DateTime":
        if v.endswith("Z"):
            v = f"{v[:-1]}+00:00"

        try:
            formatted_v = datetime.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid RFC 3339 timestamp: {v}") from e

        return cls(
            formatted_v.isoformat(timespec="seconds").replace("+00:00", "Z")
        )

    def __repr__(self):
        return f"DateTime({super().__repr__()})"


class DisplayText(dict):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: dict(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "DisplayText":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: dict) -> "DisplayText":
        if not isinstance(v, dict):
            raise TypeError(f"excpected dict but received {type(v)}")
        if "language" not in v:
            raise TypeError('property "language" required')
        if "text" not in v:
            raise TypeError('property "text" required')
        if len(v["text"]) > 512:
            raise TypeError("text too long")
        return cls(v)

    def __repr__(self):
        return f"DisplayText({super().__repr__()})"


class Number(float):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: float(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "Number":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: float | int) -> "Number":
        if not any([isinstance(v, float), isinstance(v, int)]):
            raise TypeError(f"excpected float but received {type(v)}")
        return cls(float(v))

    def __repr__(self):
        return f"Number({super().__repr__()})"


class Price(dict):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate_with_info,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: dict(x)
            ),
        )

    @classmethod
    def validate_with_info(cls, v: Any, _info: Any) -> "Price":
        return cls.validate(v)

    @classmethod
    def validate(cls, v: dict) -> "Price":
        if not isinstance(v, dict):
            raise TypeError("dictionary required")
        if "excl_vat" not in v:
            raise TypeError('property "excl_vat" required')
        return cls(v)

    def __repr__(self):
        return f"Price({super().__repr__()})"
