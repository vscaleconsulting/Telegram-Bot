from random import randint

from telethon.sessions import StringSession
import argparse
from scrapers.clients import *


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
        str_sessions_tuple.append((x[-2].rstrip().replace(' ', ''), x[-1].rstrip()))
ph_dict = dict(str_sessions_tuple)
# print(ph_dict)
s = ph_dict[ph_no.rstrip().replace(' ', '')]

api_id = 4474910
api_hash = 'cfbdbe89026e2564b1e22b9da92055b3'

cl = TGClient(StringSession(s), api_id, api_hash)
# print(s)
fname_list = ['Olivia', 'Emma', 'Ava', 'Sophia', 'Isabella', 'Charlotte', 'Amelia', 'Mia', 'Harper',
              'Evelyn', 'Abigail', 'Emily', 'Ella', 'Elizabeth', 'Camila', 'Luna', 'Sofia', 'Avery', 'Mila',
              'Aria', 'Scarlett', 'Penelope', 'Layla', 'Chloe', 'Victoria', 'Madison', 'Eleanor', 'Grace',
              'Nora', 'Riley', 'Zoey', 'Hannah', 'Hazel', 'Lily', 'Ellie', 'Violet', 'Lillian', 'Zoe',
              'Stella', 'Aurora', 'Emilia', 'Everly', 'Leah', 'Aubrey', 'Willow', 'Addison',
              'Lucy', 'Audrey', 'Bella']
cl.update_profile(fname_list[randint(0, len(fname_list))], "(VSCALE)", "SENIOR CONSULTANT 👉🏻 @vscaleconsulting 👈🏻")
cl.update_picture('dm_me.jpg')
