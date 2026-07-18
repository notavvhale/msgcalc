import json

from services.ai.client import ask
from services.ai.parser import parse_json


def select_best(product: str, candidates: list[dict]):

    if not candidates:
        return None

    candidates_text = ""

    for i, item in enumerate(candidates, start=1):

        candidates_text += f"""
Вариант {i}

Код: {item["code"]}

Описание:
{item["description"]}

Пошлина:
{item["duty_text"]}

НДС:
{item["vat"]}

----------------------------------------
"""

    prompt = f"""
Ты являешься экспертом по классификации товаров ТН ВЭД ЕАЭС.

Пользователь хочет определить код товара.

Товар:

{product}

Ниже приведены возможные варианты.

Используй ТОЛЬКО эти варианты.

Никогда не придумывай новый код.

Выбери наиболее подходящий.

Ответь ТОЛЬКО JSON.

Формат ответа:

{{
    "code":"8471300000",
    "confidence":97,
    "reason":"краткое объяснение"
}}

Варианты:

{candidates_text}
"""

    response = ask(prompt)

    data = parse_json(response)

    return data