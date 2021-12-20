
from scrapers.clients import TGClient
import csv
from config import api_id,api_hash
from telethon.sessions import StringSession
import spintax


def get_sessions(filename):
    sessions = list()
    with open(filename,encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            sessions.append(row[-1])
    
    return sessions[1:]

def ask_args():
    campaign_file = str(input("Campaign FileName: "))
    session_file = str(input("Sessions Filename: "))
    iter_range = str(input("Range [--eg: 1:10 from group 1-10 in csv] default=all: "))
    
    if iter_range==None:
        iter_range=="all"
    
    return campaign_file,session_file,iter_range
    

if __name__ =='__main__':
    
    #fetch telegram name form csv
    
    campaign_file_loc,session_file_loc,iter_range = ask_args()
    
    telegram_groups = list()
    campaign_file = open(campaign_file_loc,encoding='utf8')
    csvreader = csv.reader(campaign_file)
    
    
    
    for row in csvreader:
        link = row[5]
        try:
            if link[-1] == "/":
                link = link[:-1]
        except:
            continue         #if link is invalid dont append it        
        telegram_group_name = link.split("/")[-1]
        
        telegram_groups.append(telegram_group_name)
        
    campaign_file.close()    
    
    # fetching group names done
    
    sessions = get_sessions(session_file_loc)
    s_len = len(sessions) 
    
    iter_session = 1
    for grp in telegram_groups[1:]:       
         
        if iter_session==s_len:
            iter_session = 1
        
        bot = TGClient(StringSession(sessions[iter_session]),api_id,api_hash)
        admins = bot.get_admins(group="test125879")
        print(len(admins))
        for admin in admins:     
            message = "Hi {}, {} you're an admin for {} group! {} ask you a question as I was really curious? Can I ask It?"
            admin_name = admin.first_name
            group_name = grp
    
            arg1 = "{noticed|just saw}"
            arg2 = "{I wanted to|so i thought to reach out to you as i would like to}"
            message = message.format(admin_name,arg1,group_name,arg2)
            
            message = spintax.spin(message)
            bot.send_message(admin,message)
            print(f"sended message to {admin_name} of {group_name}")
            
        iter_session+=1

   

