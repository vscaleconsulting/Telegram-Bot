#! C:\Users\kosha\AppData\Local\Programs\Python\Python39\python.exe

from telethon.sessions import StringSession
from scrapers.clients import *
from scrapers.functions import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvs", help="list of csv files", nargs="+", type=str)
    parser.add_argument("--numbers", help="bot numbers", nargs="+", type=str)
    args = parser.parse_args()

    csvs = args.csvs
    bots = args.numbers
    bot = 0

    with open('session_ids.csv') as f:
        str_sessions_tuple = list()
        lines = f.readlines()
        for line in lines[1:]: 
            x = line.split(',')
            str_sessions_tuple.append((x[-2].rstrip().replace(' ', ''), x[-1].rstrip()))
    ph_dict = dict(str_sessions_tuple)

    status = pd.read_csv('status.csv')

    break_loop = False
    for i, row in status.iterrows():
        csv = row['file_name']
        if csv not in csvs:
            continue
        file = 'splits/' + csv
        start = 0
        f = False
        df = pd.read_csv(file)
        while not f:
            if bot == len(bots):
                break_loop = True
                break
            number = bots[bot].replace(' ', '')
            session_str = ph_dict[bots[bot].replace(' ', '')]
            cl = TGClient(StringSession(session_str), api_id, api_hash)
            df, f, start, _ = contact_admins(df, cl, start, session_str)

            status['sender_no'].iloc[i] = ('' if pd.isna(row['sender_no']) else row['sender_no'] + ';') + bots[bot]

            if not f:
                bot += 1

        df.to_csv('splits/' + csv, index=False)
        bot += 1
        if break_loop:
            break
        status['status'].iloc[i] = True
    status.to_csv('status.csv', index=False)
