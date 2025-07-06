import requests 
import util as u 
import json
config = u.Util.get_config() 
 
def get_solver_key() -> str: 
    return config["S_solverKey"] 
 
def get_token(roblox_session: requests.Session, blob: str, proxy: str, cookie) -> str:
    import time
    session = requests.Session()

    if isinstance(cookie, str):
        try:
            cookie = json.loads(cookie)
        except json.JSONDecodeError:
            cookie = dict(item.strip().split("=", 1) for item in cookie.split(";"))

    try:
        task = session.post(
            "https://syllara.com/createTask",
            json={
                "preset": "roblox_register",
                "proxy": proxy,
                "blob": blob,
                "api_key": get_solver_key(),
                "custom_cookies": cookie
            },
            timeout=60
        ).json()
        # print(task)
        while True: 
            token = session.post( 
                "https://syllara.com/getTask", 
                json={"task_id": task["task_id"]}, 
                timeout=60
            ).json() 
 
            if token.get("status") == "completed":
                # print(token)
                return token["token"] 
 
    except requests.RequestException as e: 
        print(f"[custom_solver] HTTP error occurred: {e}") 
        return None 
    except Exception as e: 
        print(f"[custom_solver] Unexpected error: {e}") 
        return None
