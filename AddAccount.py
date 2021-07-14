import random

from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.errors import PhoneNumberBannedError
from SmsPvaService import SmsPvaService
from config import api_id, api_hash


async def order_for_account():
    d = {}
    sms_service = SmsPvaService()
    data = sms_service.purchase_number()
    if data != -1:
        orderId = data['orderId']
        number = data['number']
        c_code = data['countryShortName']
        # Create Telegram Account
        client = TelegramClient(StringSession(), api_id=api_id, api_hash=api_hash)
        await client.connect()
        print(number)
        d['number'] = number

        if client.is_connected():
            try:
                code_req = await client.send_code_request(phone=number, force_sms=True)
                print(code_req)
                sms_code = sms_service.get_sms(c_code=c_code, order_id=orderId)
                if sms_code == -1:
                    return -1
                print(sms_code)
                fname_list = ['Olivia', 'Emma', 'Ava', 'Sophia', 'Isabella', 'Charlotte', 'Amelia', 'Mia', 'Harper',
                              'Evelyn', 'Abigail', 'Emily', 'Ella', 'Elizabeth', 'Camila', 'Luna', 'Sofia', 'Avery', 'Mila',
                              'Aria', 'Scarlett', 'Penelope', 'Layla', 'Chloe', 'Victoria', 'Madison', 'Eleanor', 'Grace',
                              'Nora', 'Riley', 'Zoey', 'Hannah', 'Hazel', 'Lily', 'Ellie', 'Violet', 'Lillian', 'Zoe',
                              'Stella', 'Aurora', 'Emilia', 'Everly', 'Leah', 'Aubrey', 'Willow', 'Addison',
                              'Lucy', 'Audrey', 'Bella']

                lname_list = ['(VSCALE)']
                dm_imgs = ['dm_img1.jpg', 'dm_img2.png', 'dm_img3.png', 'dm_img4.png']
                fname_pick_index = random.randint(0, len(fname_list) - 1)
                lname_pick_index = random.randint(0, len(lname_list) - 1)
                dm_pick_index = random.randint(0, len(dm_imgs) - 1)
                fname = fname_list[fname_pick_index]
                dm_img = dm_imgs[dm_pick_index]
                await client.sign_up(code=sms_code, first_name=fname, last_name=lname_list[lname_pick_index])
                await client(UploadProfilePhotoRequest(
                    await client.upload_file(dm_img)
                ))
                await client(UpdateProfileRequest(
                    about='SENIOR CONSULTANT 👉🏻 @vscaleconsulting 👈🏻'))
                await client(JoinChannelRequest('https://t.me/salesreps'))
                client_session = client.session.save()
                print(client_session)
                d['client_session'] = client_session
                await client.send_message('@vaishavdhepe', "Account Generated")

                return d

                # db_service.set_clients(phone_number=number, client_session=client_session, used_before=0)
            except PhoneNumberBannedError as e:
                print(e)
                sms_service.denial(c_code, orderId)
            except KeyboardInterrupt as e:
                print(e)
                sms_service.denial(c_code, orderId)
            except Exception as e:
                print(e)
                return -1
    return -1

# loop = asyncio.get_event_loop()
# loop.run_until_complete(order_for_account())
# order_for_account()
