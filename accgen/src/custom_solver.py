from util import Util
from time import sleep
from curl_cffi import requests
import importlib

config = Util.get_config()

SOLVER = config["solver"]
if SOLVER not in config["solverList"]:
    SOLVER = "S"
MODULE = importlib.import_module(f"{SOLVER}_solver")

def get_token(roblox_session: requests.Session, blob, proxy, cookie):
    return MODULE.get_token(roblox_session, blob, proxy, cookie)

