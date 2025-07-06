from datetime import datetime
from colorama import init, Fore
from threading import Lock

init()

lock = Lock()

class Output:
    def __init__(self, level):
        self.level = level
        self.color_map = {
            "INFO": (Fore.LIGHTCYAN_EX, "🤔"),
            "CAPTCHA": (Fore.LIGHTBLUE_EX, "🔄"),
            "ERROR": (Fore.LIGHTRED_EX, "❌"),
            "SUCCESS": (Fore.LIGHTGREEN_EX, "✅"),
            "FAVOURITE": (Fore.YELLOW, "🌟"),
            "MAIL": (Fore.RESET, "📩"),
            "HUMANIZE": (Fore.YELLOW, "👦"),
            "GROUP": (Fore.MAGENTA, "👥"),
            "FOLLOW": (Fore.YELLOW, "👦")
        }

    def log(self, *args, **kwargs):
        color, text = self.color_map.get(self.level)
        time_now = datetime.now().strftime("%H:%M:%S")

        base = f"{Fore.LIGHTBLACK_EX}[{time_now}]{Fore.RESET} ({color}{text.upper()}{Fore.RESET})"
        for arg in args:
            base += f"{color} {arg}"
        if kwargs:
            base += f"{color} {arg}"
        with lock:
            print(base)
