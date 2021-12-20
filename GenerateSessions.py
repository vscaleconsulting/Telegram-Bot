from telethon.sync import TelegramClient
from config import api_hash,api_id
from telethon.sessions import StringSession 
import requests
import csv 
import time
import random

phone = None
phone_id = None
api_key = "8A61d42e1c66750A123d7d201cbd84fb"


def cancel_activation():
    global api_key
    global phone_id
    r = requests.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=8&id={phone_id}")
    if(r.text=="ACCESS_CANCEL"):
        return True
    return False
    
    
def session_saver(client,phone,file):
    session_str = StringSession.save(client.session)
    
    writer = csv.writer(file)
    writer.writerow([phone,session_str])
    
def get_client(session_name):
    client = TelegramClient(session_name, api_id, api_hash)  
    client.connect()
    return client

def send_code(phone,client):
    try:
        client.send_code_request(phone)
    except Exception as e:
        print(e)
        cancel_activation()
        
def create_account(phone,client,code):
    try:
        client.sign_up(phone=phone, code=code, first_name="Anna")
        print("done")
    except Exception as e:
        cancel_activation()
        print("failed",e)
    

def get_number():
    
    global phone
    global phone_id
    global api_key
    
    r = requests.get(f"https://sms-activate.ru/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=tg&freePrice=true&maxPrice=10")

    if(r.status_code!=200):
        print("no numbers available")
        return 
    
    response_text = r.text
    print(response_text)
    split = response_text.split(":")
    if(len(split)!=2):
        return False #no number was found or credits exceeded
    phone,phone_id = split[-1],split[-2]
    return phone,phone_id
    

def get_code():
    global api_key
    global phone_id
    try:
        msg_sended_request = requests.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=1&id={phone_id}")
        print(msg_sended_request.text)
    except:
        pass
    time.sleep(5)
    for i in range(20):
        
        r = requests.get(f"https://api.sms-activate.org/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={phone_id}")
        status_text = r.text.split(":")
        if(status_text[0]=="STATUS_OK"):
            code = status_text[-1]
            return code
        print("retring")
        time.sleep(2)
    
    print("cancelling activation")
    cancel_activation()    
    return None

if __name__=='__main__':

    file = open("session_ids.csv","a",encoding='utf8',newline="")
    session_name = None
    
    for i in range(40): 
        session_name = f"botsession_{random.randint(0,10000)}{random.randint(0,10000)}"
        if(not get_number()):
            continue 
        client = get_client(session_name)
        send_code(phone,client)
        code = get_code()
        if(code!=None):
            print(code)
            create_account(phone,client,code)
            session_saver(client,phone,file)
        time.sleep(3)
    file.close()
    
    # file.close()