# modifys telegram accounts profile and name from sessions
from scrapers.clients import TGClient
from config import api_hash,api_id
from telethon.sessions import StringSession
import requests
import csv
import json
from random import randint
import urllib.request

def get_sessions(filename):
    '''
        returns -> list of string_sessions stored in session_ids.csv 
    '''
    session_strs = list()
    with open(filename,'r',encoding='utf8',newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            session_strs.append(row[-1])  
            
    return session_strs[1:len(session_strs)]

def get_client(str_session):
    '''
        returns -> telethon client 
    '''
    return TGClient(StringSession(str_session),api_id=api_id,api_hash=api_hash)

def get_new_face()->list:
    
    '''
        return filtered list of urls of all the faces
    '''
    
    api_key = "cX_tKbeWJZ2B-w0Krl3gKA"
    page_counter = 0 #page number to retrive, since output is not random , to make it ranadom changing the page number
    face_urls = list()
    
    # with open("AccountModifierCounter.txt","r",encoding="utf8") as f:
    #     page_counter = int(f.readline(1))
    # with open("AccountModifierCounter.txt","w",encoding="utf8") as f:
    #     f.write(f"{page_counter+1}")
    
    r = requests.get(f"https://api.generated.photos/api/v1/faces?gender=female",headers={"Authorization":f"API-Key {api_key}"})
    data = json.loads((r.content).decode("utf-8"))
    
    for faces in data["faces"]:
        url = faces["urls"][-1]["512"]
        face_urls.append(url)
    
    return face_urls
    
def generate_name():
    names = ["Alisha","Melyna","Maria","Camille","Leanne","Annetta"]
    i = 0
    while True:
        if(i>=len(names)):
            i=0
        yield(names[i])
        i+=1 

if __name__=='__main__':
    print("he")name_gen = generate_name()
    
    sessions = get_sessions('session_ids.csv')
    faces = get_new_face()
    image_counter = 1
    for session in sessions: 
        print(session)   
        client = get_client(session)
        try:
            name = name_gen.__next__()
            image = f"/images/{image_counter+1}.jpg"
            client.update_picture(image)
            client.update_profile(name[0],"(VSCALE)","SENIOR CONSULTANT 👉🏻 @vscaleconsulting 👈🏻")
            image_counter+=1
            if(image_counter==6):
                image_counter = 1
            
            client.join("salesreps")
            client.send_message('@vaishavdhepe', "Account Generated")
        except:
            continue
    