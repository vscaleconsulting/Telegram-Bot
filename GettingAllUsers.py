from scrapers.clients import *
from config import *
from telethon.tl.types import UserStatusRecently, UserStatusOnline

cl = TGClient(name='A4', api_id=api_id, api_hash=api_hash)
channel = "https://t.me/dotos"
list_of_people = [user for user in cl.get_users(channel) if not user.bot and user.username is not None and type(
    user.status) in (UserStatusRecently, UserStatusOnline)]

# for each in list_of_people:
#     print(each.username, type(each.status))

users = [each.username for each in list_of_people]
print(users)
print(len(users))
