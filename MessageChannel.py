from scrapers.clients import *
from config import *


cl = TGClient(name='A4', api_id=api_id, api_hash=api_hash)
name = 'Test2 channel0'

x = cl.send_message(name, 'hello again!')
messages = cl.pin_message(name, x.id)


