import re

from enum import IntEnum


class DutyType(IntEnum):

    FREE = 0

    ADVALOREM = 1

    SPECIFIC = 2

    MAX = 3

    SUM = 4


UNITS = {
    "кг": "kg",
    "л": "l",
    "см3": "cm3",
    "мл": "cm3",
    "м2": "m2",
    "шт": "pcs",
    "пар": "pair",
    "т": "ton",
}


def parse_duty(text: str):

    result = {
        "duty_text": text,
        "calculation_type": DutyType.FREE,

        "percent_rate": None,

        "specific_rate": None,
        "specific_currency": None,
        "specific_unit": None,
        "specific_quantity": None,
    }

    if not text:
        return result

    text = text.strip()

    if "беспошлин" in text.lower():

        return result

    # ----------------------------------------
    # %
    # ----------------------------------------

    m = re.search(
        r"(\d+(?:[.,]\d+)?)\s*%",
        text,
        re.I,
    )

    if m:

        result["percent_rate"] = float(
            m.group(1).replace(",", ".")
        )

    # ----------------------------------------
    # EUR / USD
    # ----------------------------------------

    m = re.search(
        r"(\d+(?:[.,]\d+)?)\s*(EUR|USD)\s*за\s*(\d+)?\s*([а-яА-Я0-9]+)",
        text,
        re.I,
    )

    if m:

        result["specific_rate"] = float(
            m.group(1).replace(",", ".")
        )

        result["specific_currency"] = m.group(2).upper()

        quantity = m.group(3)

        result["specific_quantity"] = (
            float(quantity)
            if quantity
            else 1
        )

        unit = m.group(4).lower()

        result["specific_unit"] = UNITS.get(
            unit,
            unit,
        )

    # ----------------------------------------
    # тип вычисления
    # ----------------------------------------

    if "плюс" in text.lower():

        result["calculation_type"] = DutyType.SUM

    elif "не менее" in text.lower():

        result["calculation_type"] = DutyType.MAX

    elif result["percent_rate"] is not None:

        result["calculation_type"] = DutyType.ADVALOREM

    elif result["specific_rate"] is not None:

        result["calculation_type"] = DutyType.SPECIFIC

    return result