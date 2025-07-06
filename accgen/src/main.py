import sys, os
import ctypes
from time import gmtime, strftime, sleep
from generate_counter import generate_counter
from generate import Generate
from threading import Thread
from util import Util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = Util.get_config()

THREAD_AMOUNT = config["threads"]
TITLE_NAME = config["titleName"]

def cpm_checker() -> None:
    elapsed = 0
    cpm_time = 0
    while True:
        generated = generate_counter.get_generated()
        cpm = round((60 / cpm_time) * generated) if cpm_time != 0 else 0
        ctypes.windll.kernel32.SetConsoleTitleW(f"Elapsed: {strftime('%H:%M:%S', gmtime(elapsed))} | CPM: {cpm} | {TITLE_NAME}")
        if generated != 0:
            cpm_time += 1
        elapsed += 1
        sleep(1)

def main() -> None:
    threads = []
    for _ in range(THREAD_AMOUNT):
        t = Thread(target=Generate.gen, args=(generate_counter,))
        threads.append(t)
        t.start()
    Thread(target=cpm_checker).start()

if __name__ == "__main__":
    main()


    
