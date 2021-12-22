
from scrapers.clients import TGClient
import csv
from config import api_id,api_hash
from telethon.sessions import StringSession
import spintax
import pandas as pd


def get_sessions(filename,session_range):
    sessions = list()
    with open(filename,encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            sessions.append(row[-1])
    
    return sessions[1:session_range]

def ask_args():
    campaign_split_number = int(input("Campaign Split Number: "))
    session_file = str(input("Sessions Filename: "))
    session_range = int(input("How Many Sessions to use: "))
    iter_range = str(input("Range [--eg: 1:10 from group 1-10 in csv] default=all: "))
    
    if iter_range==None:
        iter_range=="all"
    
    return campaign_split_number,session_file,session_range,iter_range

def get_legit_admin(group):
    admins = bot.get_admins(group=group)
    #if admin has username return it
    for admin in admins:
        if(admin.username):
            return admin
        


if __name__ =='__main__':
    
    #fetch telegram name form csv
    
    campaign_split_number,session_file_loc,session_range,iter_range = ask_args()
    
    telegram_groups = list()
    df = pd.DataFrame(pd.read_csv(f"splits/Campaign_split_{campaign_split_number}.csv"))
    telegram_groups = []
    
    
    for row in df.iloc[:,5]:
        link = row
        try:
            if link[-1] == "/":
                link = link[:-1]
        except:
            continue         #if link is invalid dont append it        
        telegram_group_name = link.split("/")[-1]
        telegram_groups.append(telegram_group_name)
        

    
    # fetching group names done
    print(telegram_groups)
    sessions = get_sessions(session_file_loc,session_range)
    s_len = len(sessions)
    
    admin_names = []
    admin_urls = []
    iter_session = 1
    for grp in telegram_groups:       
        if iter_session==s_len:
            iter_session = 1
        
        bot = TGClient(StringSession(sessions[iter_session]),api_id,api_hash)
        admin = get_legit_admin(grp)


        message = "Hi {}, {} you're an admin for {} group! {} ask you a question as I was really curious? Can I ask It?"
        admin_name = admin.first_name
        group_name = grp
        
        admin_names.append(admin.username)
        admin_urls.append(f"https://t.me/{admin.username}")
        
        arg1 = "{noticed|just saw}"
        arg2 = "{I wanted to|so i thought to reach out to you as i would like to}"
        message = message.format(admin_name,arg1,group_name,arg2)
            
        message = spintax.spin(message)
        # bot.send_message(admin,message)
        print(f"sended message to {admin_name} of {group_name}")
            
        iter_session+=1
    
   
    print(admin_names)
    print(admin_urls)
    df.columns = ["id","channel id","channel name","description","admin name","admin url"]
    df["admin name"] = admin_names
    df["admin url"] = admin_urls

    df.to_csv("splits/Campaign_split_1.csv")