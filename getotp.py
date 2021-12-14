from telethon.sync import TelegramClient
from config import api_hash,api_id


client = TelegramClient('asas', api_id, api_hash)
client.start()
channel_username = 'Telegram'# your channel
for message in client.get_messages(channel_username, limit=10):
    print(message.message)