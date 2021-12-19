import requests
from requests.api import request
from scrapers.clients import TGClient
from scrapers import functions
from telethon.sessions import StringSession 
from config import api_id,api_hash
import csv
import telethon


def scrape_coin_market_cap(start):
    
    csvfile = open("Campaign.csv",'a',encoding="utf8",newline="")
    data = functions.get_data(start,batch_size=900,__json=True)["data"]
    
    counter = start
    
    for key in data:
        
        try:
            print(counter)
            counter+=1
            coin = data[key]
            chat_urls = coin["urls"]["chat"]
            telegram_url = None
            
            
            
                
                
            
            '''continue if chats is empty'''
            if(len(chat_urls)==0):
                continue
            
            for url in chat_urls:
                if url.split("/")[-2]=="t.me":
                    telegram_url = url
            
            '''continue if chat do not contain telegram url'''     
            if telegram_url==None:
                continue
            
            grp_name = coin["name"]
            symbol = coin["symbol"]
            description = coin["description"]
            website = coin["urls"]["website"][0]
            telegram_chat = telegram_url
        
        
            csvWriter = csv.writer(csvfile) 
            field = [key,grp_name,symbol,description,website,telegram_chat]
            csvWriter.writerow(field)
        
            
            print("group appended")
        except:
            continue
        
    csvfile.close()
    return counter #returning where it ended
    

if __name__=='__main__':
    
    '''
        bot for genrating campaign from coinmarket cap
    '''
   
    
    start=9000
    while(True):
        start = scrape_coin_market_cap(start) 
