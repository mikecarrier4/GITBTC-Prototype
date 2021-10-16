# Import the requests library 
import class_list as c
import requests 
import time
import engine as e
import Utility as u
import BuySell as bs
import os
from dotenv import load_dotenv
import robin_stocks.robinhood as r


load_dotenv()



def time_wait(seconds):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            break

import sys 

print('hello')

empty_string = str(sys.argv[1:])
empty_string = empty_string.strip('["<SecureCokkieSession ')
empty_string = empty_string.strip('>"]')
dict = eval(empty_string)
print(type(dict))
print(len(dict))
print('this fucking ran')
print(dict)
print(dict['Crypto'])

#user id, job running, job time , cyrpto, strategy
