import requests

from services.ai.auth import get_token
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MODEL = "GigaChat-2"


def _request(prompt: str, token: str):

    response = requests.post(
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={
            "model": MODEL,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        verify=False,
        timeout=120,
    )

    return response


def ask(prompt: str):

    token = get_token()

    response = _request(prompt, token)

    # Если токен истёк — автоматически обновляем
    if response.status_code == 401:
        token = get_token(force=True)
        response = _request(prompt, token)

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]