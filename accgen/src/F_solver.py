
from util import Util
from curl_cffi import requests
from json import dumps
from typing import Optional

config = Util.get_config()
SOLVER_KEY = config["F_solverKey"]

def get_token(session: requests.Session, blob: str, proxy: str, cookie: str) -> Optional[str]:
    if not isinstance(session, requests.Session):
        raise TypeError("session must be an instance of requests.Session!")
    headers = {
        "Content-Type": "application/json",
        "Cookie": cookie,
        "User-Agent": session.headers.get("User-Agent", ""),
        "Sec-CH-UA": session.headers.get("Sec-CH-UA", ""),
        "Sec-CH-UA-Platform": session.headers.get("Sec-CH-UA-Platform", ""),
        "Sec-CH-UA-Mobile": session.headers.get("Sec-CH-UA-Mobile", ""),
    }
    if not headers["User-Agent"]:
        raise ValueError("missing user agent")
    payload = {
        "clientKey": SOLVER_KEY,
        "task": {
            "type": "FunCaptchaTask",
            "websiteURL": "https://www.roblox.com",
            "websitePublicKey": "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
            "proxy": proxy,
            "extraData": dumps({"blob": blob}),
            "headers": {k: v for k, v in headers.items() if v}
        }
    }
    res = requests.Session().post(
        "https://api.funbypass.com/automation/solve",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=180
    )
    if res.status_code != 200:
        print(res.content)
        return None
    try:
        print(res.json())
        return res.json().get("solution")
    except ValueError:
        return None


