from scrapers.clients import TGClient
from scrapers import functions
from telethon.sessions import StringSession 
from config import api_id,api_hash
import csv
import telethon

# gets first session string from session_ids for tgclient
def get_session(filename):
    sessions = list()
    with open(filename,encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            sessions.append(row[-1])
    
    return sessions[1:]
            
            
# gets all admins from a telegram group 
def get_admins(session_str,telegram_link=None):
    if(not telegram_link):
        return None
    group = telegram_link.split("/")[-1]
    bot = TGClient('anon',api_id,api_hash)
    
    # can conflict with message.py
    admins = bot.get_admins(group=group)

    admins_data = []
  
    if(type(admins)!=telethon.helpers.TotalList):
        return None
    
    for admin in admins:
        if admin.bot: # we dont want bots
            continue
        try:
            username = admin.username
            if(not username):
                username = "anon"
            
            name = admin.first_name
            
            admins_data.append([name,f"https://t.me/{username}"])
        
        except:
            print("user does not have username log:info")
            
    return admins_data

    
    

if __name__=='__main__':
    
    '''
        bot for genrating campaign from coinmarket cap
    '''

    csvfile = open("newCampaign.csv",'a',encoding="utf8",newline="")
    data = functions.get_data(__json=True)["data"]
    session_list = get_session("session_ids.csv")
    session_id = 2
    counter = 0
    skipper = 0
    
    for key in data:
        skipper+=1
        if(skipper<0):
            print(skipper)
            continue
        print(counter)
        coin = data[key]
        chat_urls = coin["urls"]["chat"]
        telegram_url = None
        
        
        if(counter==500):
            if(session_id==len(session_list)):
                session_id = 0
            session_id+=1
            counter=0
            
            
        
        '''continue if chats is empty'''
        if(len(chat_urls)==0):
            continue
        
        for url in chat_urls:
            if url.split("/")[-2]=="t.me":
                telegram_url = url
         
        '''continue if chat do not contain telegram url'''     
        if telegram_url==None:
            continue
        
        grp_name = coin["name"][0]
        symbol = coin["symbol"]
        description = coin["description"]
        website = coin["urls"]["website"][0]
        telegram_chat = telegram_url
        print(telegram_chat)
        admins = get_admins(session_list[session_id],telegram_chat)
    
        if(admins==None): # if a group doent contain any non bot admin
            continue
        
    
        csvWriter = csv.writer(csvfile) 
        for admin_name,admin_url in admins:
            field = [key,grp_name,symbol,description,website,telegram_chat,admin_name,admin_url]
            csvWriter.writerow(field)
            counter+=1    
        
        print("group appended")
        
    csvfile.close()