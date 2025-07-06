from util import Util
from curl_cffi import requests

config = Util.get_config()

SOLVER_KEY = config["C_solverKey"]
API_URL = "https://api.captchasolver.ai/api/solve"

def get_token(roblox_session: requests.Session, blob, proxy, cookie):
    session = requests.Session()

    api_proxy_payload = ""
    if proxy:
        if not proxy.startswith("http://") and not proxy.startswith("https://"):
            api_proxy_payload = f"http://{proxy}"
        else:
            api_proxy_payload = proxy

    payload = {
        "method": "roblox_signup",
        "proxy": api_proxy_payload,
        "blob": blob,
        "key": SOLVER_KEY,
        "browser": "firefox",
        "version": 139,
        "os": "windows"
    }

    try:
        response = session.post(API_URL, json=payload, timeout=120)

        if response.status_code == 200:
            try:
                response_data = response.json()
            except ValueError:
                return None
            
            token = response_data.get("token")
            if token:
                return token
            else:
                print(response_data)
                return None
        else:
            return None
        
    except Exception as e:
        return None
