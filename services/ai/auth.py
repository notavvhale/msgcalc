import os
import time
import uuid
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")
SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

_TOKEN = None
_EXPIRES = 0


def get_token(force=False):

    global _TOKEN
    global _EXPIRES

    if (
        not force
        and _TOKEN is not None
        and time.time() < _EXPIRES - 60
    ):
        return _TOKEN

    response = requests.post(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Authorization": f"Basic {AUTH_KEY}",
            "RqUID": str(uuid.uuid4()),
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "scope": SCOPE
        },
        verify=False,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    _TOKEN = data["access_token"]

    # expires_at приходит в миллисекундах
    _EXPIRES = data["expires_at"] / 1000

    return _TOKEN