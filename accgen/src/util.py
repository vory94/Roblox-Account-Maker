import sys, os
from string import digits, ascii_letters
from random import choice, randint
from json import load

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with open("input/proxies.txt", "r", encoding="utf-8") as file:
    proxies = file.readlines()

with open("input/config.json", "r", encoding="utf-8") as file:
    config = load(file)

class Util:
    @staticmethod
    def get_random_proxy() -> str:
        return choice(proxies).strip("\n")
    
    @staticmethod
    def get_config() -> dict:
        return config
    
    @staticmethod
    def get_random_string() -> str:
        return ''.join([choice(ascii_letters + digits) for _ in range(randint(12, 20))])
    
    @staticmethod
    def sort_dict_order(input_dict: dict) -> dict:
        keys_order = [
            "Host",
            "Connection",
            "rblx-challenge-metadata"
            "sec-ch-ua-platform",
            "Upgrade-Insecure-Requests",
            "x-csrf-token"
            "sec-ch-ua",
            "rblx-challenge-id",
            "rblx-challenge-type"
            "sec-ch-ua-mobile",
            "User-Agent",
            "Accept",
            "Content-Type",
            "Origin",
            "Sec-Fetch-Site",
            "Sec-Fetch-Mode",
            "Sec-Fetch-User",
            "Sec-Fetch-Dest",
            "Referer",
            "Accept-Language",
            "priority",
            "Cookie",
            "Accept-Encoding",
            "Content-Length"
        ]

        ordered_dict = {key: input_dict[key] for key in keys_order if key in input_dict}

        remaining_keys = {key: value for key, value in input_dict.items() if key not in keys_order}
        ordered_dict.update(remaining_keys)

        return ordered_dict