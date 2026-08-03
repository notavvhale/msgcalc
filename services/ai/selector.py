import json

from services.ai.client import ask
from services.ai.parser import parse_json


def rank_candidates(product: str, candidates: list[dict]):

    if not candidates:
        return []

    candidates_text = ""

    for i, item in enumerate(candidates, start=1):

        candidates_text += f"""
Вариант {i}

Код:
{item["code"]}

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

Необходимо определить наиболее подходящие коды ТН ВЭД.

Описание товара:

{product}

Ниже приведён список возможных вариантов.

Используй ТОЛЬКО эти варианты.

Запрещено:

- придумывать новые коды;
- изменять существующие коды;
- возвращать варианты, которых нет в списке.

Необходимо:

1. Проанализировать каждый вариант.
2. Отсортировать варианты от наиболее подходящего к менее подходящему.
3. Вернуть максимум 5 вариантов.

Ответ вернуть ТОЛЬКО в формате JSON.

[
    {{
        "code":"8471300000",
        "confidence":96,
        "reason":"Краткое объяснение выбора."
    }},
    {{
        "code":"8471410000",
        "confidence":74,
        "reason":"Почему тоже подходит."
    }}
]

Варианты:

{candidates_text}
"""

    response = ask(prompt)

    data = parse_json(response)

    if isinstance(data, dict):
        data = [data]

    return data