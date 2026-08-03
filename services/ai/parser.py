import json
import re


def parse_json(text: str):

    if not text:
        raise ValueError("Пустой ответ модели")

    # убрать markdown
    text = text.replace("```json", "")
    text = text.replace("```", "")

    text = text.strip()

    # Найти первый JSON (массив или объект)
    match = re.search(
        r"(\[.*\]|\{.*\})",
        text,
        flags=re.DOTALL,
    )

    if match:
        text = match.group(1)

    # Удалить запятые перед } и ]
    text = re.sub(
        r",\s*([}\]])",
        r"\1",
        text,
    )

    # Иногда модель ставит лишнюю запятую после массива
    text = re.sub(
        r"\]\s*,\s*$",
        "]",
        text,
    )

    # Иногда после объекта
    text = re.sub(
        r"\}\s*,\s*$",
        "}",
        text,
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError as e:

        print("=" * 80)
        print("Не удалось разобрать JSON")
        print("=" * 80)
        print(text)
        print("=" * 80)

        raise ValueError(
            f"Некорректный JSON от модели: {e}"
        ) from e