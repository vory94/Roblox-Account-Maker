from random import choice
from curl_cffi import requests
from ip_intelligence import IpIntelligence
from util import Util

class Session:
    @staticmethod
    def session() -> requests.Session:
        browsers = [
            ("chrome", '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        ]

        browser = choice(browsers)

        session = requests.Session(
            impersonate=browser[0],
            akamai="1:65536;2:0;4:6291456;6:262144|15663105|0|m,a,s,p",
            extra_fp={
                "tls_signature_algorithms": [
                    "ecdsa_secp256r1_sha256",
                    "rsa_pss_rsae_sha256",
                    "rsa_pkcs1_sha256",
                    "ecdsa_secp384r1_sha384",
                    "rsa_pss_rsae_sha384",
                    "rsa_pkcs1_sha384",
                    "rsa_pss_rsae_sha512",
                    "rsa_pkcs1_sha512"
                ],
                "tls_grease": True,
                "tls_permute_extensions": True
            },
            verify=False
        )

        proxy = Util.get_random_proxy()

        session.proxies = {
            "http": proxy,
            "https": proxy
        }

        session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': "en-US,en;q=0.9",
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.roblox.com',
            'priority': 'u=0, i',
            'sec-ch-ua': browser[1],
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            'User-Agent': browser[2],
            'Upgrade-Insecure-Requests': '1'
        }

        session.headers["Accept-Language"] = IpIntelligence(session).get_accept_language()

        session.headers = Util.sort_dict_order(session.headers)

        return session
    
    @staticmethod
    def set_page_request_headers(headers: dict) -> dict:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        headers["priority"] = 'u=0, i'
        headers["Sec-Fetch-Dest"] = "document"
        headers["Sec-Fetch-User"] = "?1"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "same-origin"
        headers['Upgrade-Insecure-Requests'] = '1'
        
        headers = Util.sort_dict_order(headers)

        return headers

    @staticmethod
    def set_iframe_request_headers(headers: dict) -> dict:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        headers["priority"] = 'u=0, i'
        headers["Sec-Fetch-Dest"] = "iframe"
        headers["Sec-Fetch-User"] = "?1"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "same-origin"
        headers['Upgrade-Insecure-Requests'] = '1'

        headers = Util.sort_dict_order(headers)

        return headers

    @staticmethod
    def set_image_request_headers(headers: dict) -> dict:
        keys = headers.keys()

        if 'Upgrade-Insecure-Requests' in keys:
            headers.pop('Upgrade-Insecure-Requests')
        if 'Sec-Fetch-User' in keys:
            headers.pop('Sec-Fetch-User')
        
        headers["Accept"] = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
        headers["priority"] = 'u=2, i'
        headers["Sec-Fetch-Dest"] = "image"
        headers["Sec-Fetch-Mode"] = "no-cors"
        headers["Sec-Fetch-Site"] = "same-origin"

        headers = Util.sort_dict_order(headers)

        return headers

    @staticmethod
    def set_api_request_headers(headers: dict) -> dict:
        keys = headers.keys()

        if 'Upgrade-Insecure-Requests' in keys:
            headers.pop('Upgrade-Insecure-Requests')
        if 'Sec-Fetch-User' in keys:
            headers.pop('Sec-Fetch-User')

        headers["Accept"] = "application/json, text/plain, */*"
        headers["priority"] = 'u=1, i'
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-site"

        headers = Util.sort_dict_order(headers)

        return headers