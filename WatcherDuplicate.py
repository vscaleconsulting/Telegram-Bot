from telethon.sessions import StringSession
from config import *
from scrapers.clients import *
from scrapers.functions import *

file = 'splits/Campaign_split_1.csv'
df = pd.read_csv(file)

for i, row in tqdm(df.iterrows()):
    if row['delivered']:
        cl = TGClient(StringSession(row['session_str']), api_id, api_hash)
        forwards = list()
        messages = list()
        for message in cl.get_chat_messages(row['admin_contact_url'], None):
            if not message.out:
                forwards.insert(0, message)
                messages.append(message.message)
                print(message.message)
            else:
                break
        if len(forwards) > 0:
            df['replied'].iloc[i] = True
            df['reply'].iloc[i] = messages
            # cl.forward_messages(RECIPIENT, forwards)
            print(row['admin_contact_url'])
            print(*forwards, sep='\n')

df.to_csv(file, index=False)
