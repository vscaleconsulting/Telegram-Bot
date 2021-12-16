#! C:\Users\kosha\AppData\Local\Programs\Python\Python39\python.exe
from telethon.sessions import StringSession
import argparse
from config import *
from scrapers.clients import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()[1]

    if len(args):
        ph_no = args[0] 
    else:
        ph_no = input('Enter number: ')
    with open('session_ids.csv') as f:
        str_sessions_tuple = list()
        lines = f.readlines()
        for line in lines[1:]:
            x = line.split(',')
            try:
                str_sessions_tuple.append((x[-2].rstrip().replace(' ', ''), x[-1].rstrip()))
            except:
                continue
            
    ph_dict = dict(str_sessions_tuple)
    str_session_id = ph_dict[ph_no.rstrip().replace(' ', '')]
    try:
        str_session_id = ph_dict[ph_no]
    except:
        print('Invalid Number')
        exit()

    cl = TGClient(StringSession(str_session_id), api_id, api_hash)
    forwards = list()

    for message in cl.get_chat_messages(777000, 1):
        if not message.out:
            forwards.insert(0, message)
            print(message.message)
    # cl.forward_messages(RECIPIENT, forwards)
