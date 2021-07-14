from scrapers.clients import *
from config import *
from telethon.tl.patched import Message

from scrapers.functions import *

cl = TGClient(name='A4', api_id=api_id, api_hash=api_hash)
source = 'Test2 channel0'  # 1190866096
dests = [f'Practice channel{i}' for i in range(1, 21)]  # 1459494145

for dest in dests:
    # print(cl.get_link(dest).link)
    forward_new_messages(cl, source, dest)
