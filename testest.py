from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, UserStatusOnline, UserStatusRecently
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser

import traceback
import time
from tqdm import tqdm
import random

from scrapers.clients import TGClient

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

api_id = 1868530
api_hash = "edf7d1e794e0b4a5596aa27c29d17eba"
phone = '+79058102761'
client = TelegramClient('A9', api_id, api_hash)
# client = TGClient('A9', api_id, api_hash)

client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)

    # banner()
    # client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))
n = 0

target_channel = "https://t.me/cryptoinsiderslimited"

users = ["PandaIf", "Imang0102", "thekmills"]

# for user in users:
#     x = client.invite_to_channel(target_channel, [user])
#     print(x)
# exit()

for user in tqdm(users[:500]):
    print(user)
    n += 1
    if n % 40 == 0:
        time.sleep(900)
    try:
        print("Adding {}".format(user))
        # user_to_add = client.get_input_entity(user)
        client(InviteToChannelRequest(channel=target_channel, users=[user]))
        print(gr + "[+] Waiting for right time to add members...")
        time.sleep(random.randrange(60, 180))
    except PeerFloodError:
        print(
            re + "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again "
                 "after some time.")
        # time.sleep(60 * 15)
        exit()
    except UserPrivacyRestrictedError:
        print(re + "[!] The user's privacy settings do not allow you to do this. Skipping.")
        # time.sleep(random.randrange(0, 30))
    except:
        traceback.print_exc()
        print(re + "[!] Unexpected Error")
