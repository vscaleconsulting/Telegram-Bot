import asyncio
import pandas as pd
from AddAccount import *
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("count", help="number of accounts", type=int)
parser.add_argument("csv", help="csv filename", type=str)
args = parser.parse_args()
n = args.count
file_name = args.csv

df = pd.read_csv(file_name)
target = df.shape[0] + n
attempts = 0
max_attempts = 5

while df.shape[0] < target:
    print(attempts)
    if attempts == max_attempts:
        attempts = 0
        print('Waiting for 10 mins...')
        sleep(10*60)
    attempts += 1
    loop = asyncio.get_event_loop()
    d = loop.run_until_complete(order_for_account())
    if d != -1:
        attempts = 0
        df = df.append(d, ignore_index=True)
        df.to_csv(file_name, index=False)

