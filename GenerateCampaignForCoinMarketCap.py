#! C:\Users\kosha\AppData\Local\Programs\Python\Python39\python.exe

from scrapers.functions import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("admin_count", help="Number of admins per Entry (Defaults to All)", nargs='?', type=int)
    args = parser.parse_args()
    campaign_file = 'Campaign.csv'
    df = pd.read_csv('final_solution4000.csv')

    r = generate_messages(df, message, args.admin_count, additional_cols=['id', 'name', 'symbol', 'description', 'website'])
    
    r.to_csv(campaign_file, index=False)
