#! C:\Users\kosha\AppData\Local\Programs\Python\Python39\python.exe

from scrapers.functions import *
import argparse
from config import *

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("admin_count", help="Number of admins per Entry (Defaults to All)", nargs='?', type=int)
    # args = parser.parse_args()
    try:
        os.mkdir(PATH_CAMPAIGN_LIST)
    except:
        pass
    entries = os.listdir(PATH_ADMIN_LIST)

    i = input('Number of admins per Entry: ')
    admin_count = int(i) if i != '' else 1

    for f in entries:
        print(f'Processing {f}')
        site = f.split('_')[-1].split('.')[0]
        campaign_file = PATH_CAMPAIGN_LIST + f'CampaignFor{site}.csv'

        adminlist_file = f'AdminLists/Adminlist_{site}.csv'

        df = pd.read_csv(adminlist_file)

        try:
            cdf = pd.read_csv(campaign_file)
            end = df.index[df['title_of_press_release'] == cdf['title_of_press_release'].iloc[0]][0]
            df = df[:end]
        except:
            cdf = pd.DataFrame()

        r = generate_messages(df, message2, admin_count, additional_cols=['name_of_project', 'title_of_press_release'])
        r.drop_duplicates(subset='admin_contact_url', inplace=True)
        r = pd.concat([r, cdf])
        r.to_csv(campaign_file, index=False)
