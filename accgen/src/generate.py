from threading import Lock
from generate_counter import GenerateCounter
from output import Output
from roblox_profile import RobloxProfile
from session import Session
from auth_intent import AuthIntent
from custom_solver import get_token
from util import Util
from json import loads, dumps
from base64 import b64encode, b64decode
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = Util.get_config()
LOCK = Lock()

class Generate:
    @staticmethod
    def gen(generate_counter: GenerateCounter) -> None:
        while True:
            try:
                username, password = RobloxProfile.get_username(), RobloxProfile.get_password()
                birthday, gender = RobloxProfile.get_birth_day(), RobloxProfile.get_gender()

                Output("INFO").log(f"Generating account {username}")

                session = Session.session()

                resp = session.get("https://www.roblox.com/")

                if resp.status_code == 429:
                    raise ValueError("Rate limited")
                
                session.headers = Session.set_image_request_headers(session.headers)
                session.headers = Util.sort_dict_order(session.headers)

                session.get("https://www.roblox.com/timg/rbx")

                if resp.status_code == 429:
                    raise ValueError("Rate limited")

                session.headers["x-csrf-token"] = resp.text.split('data-token="')[1].split('"')[0]
                session.headers = Session.set_api_request_headers(session.headers)
                session.headers = Util.sort_dict_order(session.headers)

                payload = {
                    'username': username,
                    'context': 'Signup',
                    'birthday': birthday,
                }

                resp = session.post("https://auth.roblox.com/v1/usernames/validate", json=payload)

                if resp.status_code == 429:
                    raise ValueError("Rate limited")

                while resp.status_code != 200 or resp.json()["code"] != 0:
                    username = RobloxProfile.get_username()
                    payload["username"] = username

                    resp = session.post("https://auth.roblox.com/v1/usernames/validate", json=payload)

                    csrf = resp.headers.get("x-csrf-token")

                    if csrf:
                        session.headers["x-csrf-token"] = csrf

                    if resp.status_code == 429:
                        raise ValueError("Rate limited")

                payload = {
                    'username': username,
                    'password': password
                }

                session.post("https://auth.roblox.com/v2/passwords/validate", json=payload)

                if resp.status_code == 429:
                    raise ValueError("Rate limited")

                auth_intent = AuthIntent.get_auth_intent(session)

                signup_payload = {
                    'username': username,
                    'password': password,
                    'birthday': birthday,
                    'gender': gender,
                    'isTosAgreementBoxChecked': True,
                    'agreementIds': [
                        '460f3c21-e306-4de0-949f-8e263b7210d0',
                        'b354f748-8bb4-4859-9b71-c61a63e140dc',
                    ],
                    'secureAuthenticationIntent': auth_intent
                }

                resp = session.post("https://auth.roblox.com/v2/signup", json=signup_payload)

                if resp.status_code == 429:
                    raise ValueError("Rate limited")

                challenge_id = resp.headers.get("rblx-challenge-id")
                metadata = loads(b64decode(resp.headers.get("rblx-challenge-metadata").encode("utf-8")).decode("utf-8"))
                blob = metadata.get("dataExchangeBlob")
                captcha_id = metadata.get("unifiedCaptchaId")

                cookie_header = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])

                Output("CAPTCHA").log("Solving captcha")

                solution = get_token(session, blob, session.proxies["http"], cookie_header)

                if solution == None:
                    raise ValueError("Failed to solve captcha")
                
                token = solution.split("|")[0]
                token_info = solution.split("pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F|")[1].split("|cdn_url=")[0]

                Output("CAPTCHA").log(f"Captcha solved | {token}|{token_info}")

                challenge_metadata = dumps({
                    "unifiedCaptchaId": captcha_id,
                    "captchaToken": solution,
                    "actionType": "Signup"
                }, separators=(',', ':'))

                payload = dumps({
                    "challengeId": challenge_id,
                    "challengeType": "captcha",
                    "challengeMetadata": challenge_metadata
                }, separators=(',', ':'))

                resp = session.post("https://apis.roblox.com/challenge/v1/continue", data=payload)

                if resp.status_code != 200:
                    raise ValueError("Rejected by continue API")

                session.headers["rblx-challenge-id"] = challenge_id
                session.headers["rblx-challenge-metadata"] = b64encode(challenge_metadata.encode("utf-8")).decode("utf-8")
                session.headers["rblx-challenge-type"] = "captcha"

                session.headers = Util.sort_dict_order(session.headers)

                resp = session.post("https://auth.roblox.com/v2/signup", json=signup_payload)

                if resp.status_code != 200:
                    raise ValueError("Rejected by signup API")
                
                session.headers = Session.set_page_request_headers(session.headers)
                session.headers = Util.sort_dict_order(session.headers)

                session.get("https://www.roblox.com/home?nu=true")

                generate_counter.increase_generated()

                Output("SUCCESS").log(f"Successfully generated account | {username}")

                response_cookie = resp.headers["set-cookie"]

                if type(response_cookie) == list:
                    for cookie in response_cookie:
                        if '.ROBLOSECURITY' in cookie:
                            account_cookie = cookie.split(".ROBLOSECURITY=")[1].split(";")[0]
                else:
                    account_cookie = response_cookie.split(".ROBLOSECURITY=")[1].split(';')[0]

                with LOCK:
                    filename = config["userType"]
                    with open(f"output/{filename}.txt", "a", encoding="utf-8") as file:
                        towritestr = config["outputFormat"]+"\n"
                        towritestr = towritestr.replace("USERNAME", username)
                        towritestr = towritestr.replace("PASSWORD", password)
                        towritestr = towritestr.replace("COOKIE", account_cookie)
                        file.write(towritestr)

            except Exception as e:
                if "Failed to perform" in str(e):
                    Output("ERROR").log("Error | Proxy failed to make request")
                else:
                    Output("ERROR").log(f"Error | {str(e)}")
