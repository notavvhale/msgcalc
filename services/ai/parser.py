import json
import re


def parse_json(text: str):

    text = text.strip()

    # убрать ```json
    text = re.sub(r"^```json\s*", "", text)

    # убрать ```
    text = re.sub(r"\s*```$", "", text)

    text = text.strip()

    return json.loads(text)