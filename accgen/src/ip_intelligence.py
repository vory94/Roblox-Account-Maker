from curl_cffi.requests import Session
import locale
import random

class IpIntelligence:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_accept_language(self) -> str:
        try:
            system_locale = locale.getlocale()[0] or 'en_US'
            primary_lang = system_locale.split('_')[0]
        except:
            primary_lang = 'en'

        language_variations = [
            (f"{primary_lang}-{primary_lang.upper()},en-US;q=0.9,en;q=0.8", 0.6),
            (f"{primary_lang}-{primary_lang.upper()};q=0.9,en;q=0.8", 0.2),
            (f"en-US,en;q=0.9,{primary_lang}-{primary_lang.upper()};q=0.8", 0.1),
            (f"{primary_lang},en-US;q=0.9,en;q=0.8", 0.1)
        ]

        accept_language = random.choices(
            [var[0] for var in language_variations],
            weights=[var[1] for var in language_variations],
            k=1
        )[0]

        return accept_language
