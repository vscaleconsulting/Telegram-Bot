from scrapers.functions import *
from scrapers.clients import *
from config import *
from constants import *
from random import random, choice
from time import sleep
from telethon.tl.types import UserStatusRecently, UserStatusOnline

cl = TGClient(name='A3', api_id=api_id, api_hash=api_hash)
channel = "https://t.me/pawhyred"
list_of_people = [user for user in cl.get_users(channel) if not user.bot and user.username is not None and type(
    user.status) in (UserStatusRecently, UserStatusOnline)]

dm_imgs = ['dm_img1.jpg', 'dm_img2.png', 'dm_img3.png', 'dm_img4.png']

for i in range(10):
    name = f"Holaxfd!{i}"
    cl.create_channel(name, ':)')
    x = 10 * i
    users = list_of_people[x:x + 10]

    add_users_to_channel(cl, list_of_people[x:x + 10], name)

# 1 Updates(updates=[], users=[], chats=[Channel(id=1328361097, title='Holaa!5', photo=ChatPhotoEmpty(), date=datetime.datetime(2021, 4, 30, 7, 29, 30, tzinfo=datetime.timezone.utc), version=0, creator=True, left=False, broadcast=True, verified=False, megagroup=False, restricted=False, signatures=False, min=False, scam=False, has_link=False, has_geo=False, slowmode_enabled=False, call_active=False, call_not_empty=False, fake=False, gigagroup=False, access_hash=7929474091916924632, username=None, restriction_reason=[], admin_rights=ChatAdminRights(change_info=True, post_messages=True, edit_messages=True, delete_messages=True, ban_users=True, invite_users=True, pin_messages=True, add_admins=True, anonymous=False, manage_call=True, other=True), banned_rights=None, default_banned_rights=None, participants_count=None)], date=datetime.datetime(2021, 4, 30, 7, 31, 31, tzinfo=datetime.timezone.utc), seq=0)
