from config import api_id, api_hash
from scrapers.clients import *
import pandas as pd
import os

if __name__ == '__main__':
    csv = 'session_ids.csv'
    try:
        os.remove('X.session')
    except FileNotFoundError:
        pass

    cl = TGClient('X', api_id, api_hash)
    cl.connect()
    del cl
    cl = TGClient('X', api_id, api_hash)
    sess = cl.get_session_str()
    ph = str(cl.get_me().phone)
    ph = f'+{ph[:3]} {ph[3:]}'
    df = pd.read_csv(csv)
    df = df.append({'number': ph, 'client_session': sess}, ignore_index=True)
    df.to_csv(csv, index=False)
