BAL_URL = "http://smspva.com/priemnik.php?metod=get_balance&service=opt4&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"
COUNTRY_CODE = "PT"
SERVICE_PRICE_URL = "http://smspva.com/priemnik.php?metod=get_service_price&country={}&service=opt4&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP".format(
    COUNTRY_CODE)
GET_NUMBER_URL = "http://smspva.com/priemnik.php?metod=get_number&country={}&service=opt29&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP".format(
    COUNTRY_CODE)
MAX_PRICE = 2
api_id = 1868530
api_hash = "edf7d1e794e0b4a5596aa27c29d17eba"

# api_id = 1482064
# api_hash = 'f130a32340a40482adf14858fe2ca3f9'

GET_SMS_URL = "http://smspva.com/priemnik.php?metod=get_sms&country={}&service=opt4&id=ORDER_ID&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP".format(
    COUNTRY_CODE)

COUNTRY_LIST = "https://gist.githubusercontent.com/vrushangdev/23c1dabbd6fce720e065bed302cba3f3/raw/e91258e054906f7648243b2009cac69776c12567/country_list.json"
# api_key = "PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"

PATH_ADMIN_LIST = 'AdminLists/'
PATH_CAMPAIGN_LIST = 'CampaignLists/'

PRO_API_KEY = '016f8cff-67ed-4a55-8073-a7fa5232ca31'
RECIPIENT = "https://t.me/salesreps"

PATH_TELEGRAM_PRESS_RELEASE = r'E:\Documents\GitHub\VScale\NewsScrapper\telegram'

message = "Hi <tg admin name>, {noticed|just saw} you're an admin for <name> group! {I wanted to|so i thought to reach out to you as i would like to} ask you a question as I was really curious? Can I ask It?"
message2 = "Hi <tg admin name>, Just saw ur article about '<title_of_press_release>' on '<name_of_project>', that's really amazing. I wanted to ask you a question as i was really curious"