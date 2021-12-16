# modifys telegram accounts profile and name from sessions
from scrapers.clients import TGClient
from config import api_hash,api_id
from telethon.sessions import StringSession
import requests
import csv

def get_sessions(filename):
    '''
        returns -> list of string_sessions stored in session_ids.csv 
    '''
    session_strs = list()
    with open(filename,'r',encoding='utf8',newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            session_strs.append(row[-1])  
            
    return session_strs

def get_client(str_session):
    '''
        returns -> telethon client 
    '''
    return TGClient(StringSession(str_session),api_id=api_id,api_hash=api_hash)

def get_new_face():
    api_key = "cX_tKbeWJZ2B-w0Krl3gKA"
    r = requests.get(f"https://api.generated.photos/api/v1/faces?gender=female?per_page=10",headers={"Authorization":f"API-Key {api_key}"})
    print(r.text)

if __name__=='__main__':
    # get_sessions('session_ids.csv')
    # client = get_client("1BVtsOLABu7MO2UtjY0NSyb9S6Pma7l9sFMLoxoJSIVSYX-xv5ShIHu6UAMkTlii6jlqs7ep4D0Jo1iVXoM_Kon2mW6dMzkZA0nlqvvB_3MY-CrZnUY98i55DJTphOBxNsuUhNvgph_RU_cgSujJKq5RNSU3scjk_MGyG5Ct0_jwy_PDHPn15ai-LzQkUzQhawG1lFoKYmpzk3XXjWHkp77UPgBnK2I_QIfMvjKjvdiX39YK1-9cLawGaecNPiWAX-8BNBUAJJ-FSzeT5fPfildmmCIJa8xMUcHp0tnVRPjdU9UZHjlNXDBmc7NvDEfZRbHTAQjhuggp6g2lkXyc_UdbQ2hcmpgA=")

    # client.update_profile("swapnil","shinde","hi i am swapnil shinde")
    
    get_new_face()