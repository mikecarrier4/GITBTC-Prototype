import time
import datetime

def time_wait(seconds):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            print(datetime.datetime.now())
            break

