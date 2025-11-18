from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.modules.locations.v_2_2_1.schemas import EnergyMix
from py_ocpi.modules.tariffs.v_2_2_1.enums import (
    DayOfWeek,
    ReservationRestrictionType,
    TariffDimensionType,
    TariffType,
)
from py_ocpi.core.data_types import (
    URL,
    CiString,
    DisplayText,
    Number,
    Price,
    String,
    DateTime,
)


class PriceComponent(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#142-pricecomponent-class
    """

    type: TariffDimensionType
    price: Number
    vat: Optional[Number] = None
    step_size: int


class TariffRestrictions(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#146-tariffrestrictions-class
    """

    start_time: Optional[String(5)] = None  # type: ignore
    end_time: Optional[String(5)] = None  # type: ignore
    start_date: Optional[String(10)] = None  # type: ignore
    end_date: Optional[String(10)] = None  # type: ignore
    min_kwh: Optional[Number] = None
    max_kwh: Optional[Number] = None
    min_current: Optional[Number] = None
    max_current: Optional[Number] = None
    min_power: Optional[Number] = None
    max_power: Optional[Number] = None
    min_duration: Optional[int] = None
    max_duration: Optional[int] = None
    day_of_week: List[DayOfWeek] = []
    reservation: Optional[ReservationRestrictionType] = None


class TariffElement(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#144-tariffelement-class
    """

    price_components: List[PriceComponent]
    restrictions: Optional[TariffRestrictions] = None


class Tariff(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#131-tariff-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(36)  # type: ignore
    currency: String(3)  # type: ignore
    type: Optional[TariffType] = None
    tariff_alt_text: List[DisplayText] = []
    tariff_alt_url: Optional[URL] = None
    min_price: Optional[Price] = None
    max_price: Optional[Price] = None
    elements: List[TariffElement]
    start_date_time: Optional[DateTime] = None
    end_date_time: Optional[DateTime] = None
    energy_mix: Optional[EnergyMix] = None
    last_updated: DateTime
