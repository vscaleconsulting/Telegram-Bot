from scrapers.clients import *
from constants import *
from config import *

if __name__ == '__main__':

    available = list()
    unavailable = list()

    for i, bot in enumerate(bot_tokens):
        cl = TGClient(bot, api_id, api_hash, bot_tokens[i])
        ret = cl.get_entity('https://t.me/salesreps')
        if type(ret) == int:
            unavailable.append(bot)
        else:
            available.append(bot)

    print('Available:')
    print(*available, sep=',\n', end='\n\n')
    print('Unavailable:')
    print(*unavailable, sep=',\n', end='\n\n')