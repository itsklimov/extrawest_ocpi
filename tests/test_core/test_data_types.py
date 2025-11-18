"""Minimal unit tests for py_ocpi.core.data_types validators"""
import pytest
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError

from py_ocpi.core.data_types import (
    String,
    CiString,
    URL,
    DateTime,
    DisplayText,
    Number,
    Price,
)


class TestStringValidator:
    """Test String custom validator"""

    def test_valid_string(self):
        """Test valid string within max length"""
        class Model(BaseModel):
            value: String(10)

        result = Model(value="hello")
        assert result.value == "hello"

    def test_max_length_exceeded(self):
        """Test string exceeding max length raises ValueError"""
        class Model(BaseModel):
            value: String(5)

        with pytest.raises(ValidationError, match="length must be lower or equal"):
            Model(value="toolong")

    def test_non_string_raises_error(self):
        """Test non-string input raises TypeError"""
        class Model(BaseModel):
            value: String(10)

        with pytest.raises((ValidationError, TypeError), match="excpected string"):
            Model(value=123)

    def test_utf8_string(self):
        """Test UTF-8 string is valid"""
        class Model(BaseModel):
            value: String(20)

        result = Model(value="émojis_✓")
        assert result.value == "émojis_✓"


class TestCiStringValidator:
    """Test CiString custom validator"""

    def test_valid_ascii_string(self):
        """Test valid ASCII string"""
        class Model(BaseModel):
            value: CiString(10)

        result = Model(value="HELLO")
        # Default behavior is lowercase (from settings.CI_STRING_LOWERCASE_PREFERENCE)
        assert result.value.lower() == result.value or result.value.upper() == result.value

    def test_non_ascii_raises_error(self):
        """Test non-ASCII string raises ValueError"""
        class Model(BaseModel):
            value: CiString(10)

        with pytest.raises(ValidationError, match="invalid cistring format"):
            Model(value="émoji")

    def test_max_length_exceeded(self):
        """Test exceeding max length raises ValueError"""
        class Model(BaseModel):
            value: CiString(3)

        with pytest.raises(ValidationError, match="length must be lower or equal"):
            Model(value="toolong")


class TestURLValidator:
    """Test URL custom validator"""

    def test_valid_url(self):
        """Test valid URL"""
        class Model(BaseModel):
            value: URL

        result = Model(value="http://example.com")
        assert result.value == "http://example.com"

    def test_url_max_length(self):
        """Test URL exceeding 255 chars raises ValueError"""
        class Model(BaseModel):
            value: URL

        long_url = "http://" + "a" * 250 + ".com"
        with pytest.raises(ValidationError, match="length must be lower or equal"):
            Model(value=long_url)


class TestDateTimeValidator:
    """Test DateTime custom validator"""

    def test_valid_rfc3339_with_z(self):
        """Test valid RFC 3339 timestamp with Z suffix"""
        class Model(BaseModel):
            value: DateTime

        result = Model(value="2024-01-15T10:30:00Z")
        assert result.value.endswith("Z")
        assert "2024-01-15T10:30:00Z" == result.value

    def test_valid_rfc3339_with_offset(self):
        """Test valid RFC 3339 timestamp with offset"""
        class Model(BaseModel):
            value: DateTime

        result = Model(value="2024-01-15T10:30:00+00:00")
        assert result.value.endswith("Z")
        assert "2024-01-15T10:30:00Z" == result.value

    def test_invalid_timestamp_raises_error(self):
        """Test invalid timestamp format raises ValueError"""
        class Model(BaseModel):
            value: DateTime

        with pytest.raises(ValidationError, match="Invalid RFC 3339 timestamp"):
            Model(value="not-a-timestamp")


class TestDisplayTextValidator:
    """Test DisplayText custom validator"""

    def test_valid_display_text(self):
        """Test valid display text with language and text"""
        class Model(BaseModel):
            value: DisplayText

        result = Model(value={"language": "en", "text": "Standard Tariff"})
        assert result.value["language"] == "en"
        assert result.value["text"] == "Standard Tariff"

    def test_missing_language_raises_error(self):
        """Test missing language field raises TypeError"""
        class Model(BaseModel):
            value: DisplayText

        with pytest.raises((ValidationError, TypeError), match='property "language" required'):
            Model(value={"text": "Standard Tariff"})

    def test_missing_text_raises_error(self):
        """Test missing text field raises TypeError"""
        class Model(BaseModel):
            value: DisplayText

        with pytest.raises((ValidationError, TypeError), match='property "text" required'):
            Model(value={"language": "en"})

    def test_text_too_long_raises_error(self):
        """Test text exceeding 512 chars raises TypeError"""
        class Model(BaseModel):
            value: DisplayText

        with pytest.raises((ValidationError, TypeError), match="text too long"):
            Model(value={"language": "en", "text": "a" * 513})


class TestNumberValidator:
    """Test Number custom validator"""

    def test_valid_float(self):
        """Test valid float"""
        class Model(BaseModel):
            value: Number

        result = Model(value=3.14)
        assert result.value == 3.14

    def test_valid_int(self):
        """Test valid int converted to float"""
        class Model(BaseModel):
            value: Number

        result = Model(value=42)
        assert result.value == 42.0


class TestPriceValidator:
    """Test Price custom validator"""

    def test_valid_price(self):
        """Test valid price with excl_vat"""
        class Model(BaseModel):
            value: Price

        result = Model(value={"excl_vat": 1.0, "incl_vat": 1.25})
        assert result.value["excl_vat"] == 1.0
        assert result.value["incl_vat"] == 1.25

    def test_price_without_incl_vat(self):
        """Test price with only excl_vat is valid"""
        class Model(BaseModel):
            value: Price

        result = Model(value={"excl_vat": 1.0})
        assert result.value["excl_vat"] == 1.0

    def test_missing_excl_vat_raises_error(self):
        """Test missing excl_vat raises TypeError"""
        class Model(BaseModel):
            value: Price

        with pytest.raises((ValidationError, TypeError), match='property "excl_vat" required'):
            Model(value={"incl_vat": 1.25})

    def test_non_dict_raises_error(self):
        """Test non-dict input raises TypeError"""
        class Model(BaseModel):
            value: Price

        with pytest.raises((ValidationError, TypeError), match="dictionary required"):
            Model(value="not a dict")
