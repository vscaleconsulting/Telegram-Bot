# Buy Number & Get OTP
import datetime

from config import BAL_URL
import json
import requests
import random
from time import sleep


class SmsPvaService:
    service_price_url = None
    balance_url = None
    number_url = "http://smspva.com/priemnik.php?metod=get_number&country=COUNTRY_CODE&service=opt29&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"
    sms_url = "http://smspva.com/priemnik.php?metod=get_sms&country=COUNTRY_CODE&service=opt4&id=ORDER_ID&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"
    denial_url = "http://smspva.com/priemnik.php?metod=denial&country=COUNTRY_CODE&service=opt4&id=ORDER_ID&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"

    def __init__(self):
        self.balance_url = BAL_URL
        try:
            with open('affordable_country.txt', 'r') as handle:
                text = handle.read()
            self.country_list = json.loads(text)

        except Exception as e:
            print("Exception opening file", e)

    def get_price(self, service_price_url):
        """Get Price From SMS PVA"""
        response = requests.get(url=service_price_url)
        data = json.loads(response.text)
        # print(data['price'])
        return data['price']

    def get_balance(self):
        response = requests.get(url=self.balance_url)
        data = json.loads(response.text)
        print(data['balance'])
        return data['balance']

    def purchase_number(self):
        """Purchase number from smspva"""
        for country in self.country_list:
            country = country['country']
            print(country)
            url = self.number_url.replace("COUNTRY_CODE", str(country))
            resp = requests.get(url)
            print(resp)
            print(resp.text)
            data = json.loads(resp.text)
            if data['number'] is not None:
                break
            sleep(1)
        else:
            return -1

        required_data = {'countryShortName': country, 'orderId': data['id'],
                         'number': data['CountryCode'] + " " + data['number']}
        print(data)
        print(required_data)
        return required_data

    def get_sms(self, c_code, order_id):
        """Get Sms From SmsPVA Service."""
        url = self.sms_url.replace("COUNTRY_CODE", c_code).replace("ORDER_ID", str(order_id))
        resp = requests.get(url)
        data = json.loads(resp.text)
        print(data)
        t = 0
        while data['sms'] is None:
            resp = requests.get(url)
            print(resp.text)
            data = json.loads(resp.text)
            print("Waiting for SMS...")
            sleep(5)
            t += 5
            if t == 3 * 60:
                self.denial(c_code, order_id)
                return -1
        return data['sms']

    def denial(self, c_code, order_id):
        url = self.denial_url.replace("COUNTRY_CODE", c_code).replace("ORDER_ID", str(order_id))
        while True:
            resp = requests.get(url)
            print(resp.text)
            data = json.loads(resp.text)
            if data['response'] == '1':
                return
            sleep(2)
