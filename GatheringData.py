import os
import argparse
from constants import *
from scrapers.clients import *
from scrapers.functions import *


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("start", help="start index", nargs='?', default=1)
    # parser.add_argument("limit", help="number of entries",
    #                     nargs='?', default=5000)
    # args = parser.parse_args()

    # start = 3158
    # df = get_data(args.start, args.limit)
    # df.to_csv('ids.csv', index=False)
    # # df = pd.read_csv('ids.csv')
    # prev_x = 0
    # # bot_tokens = bot_tokens[::-1]
    # for i, token in enumerate(bot_tokens):
    #     print(f'Using Bot {i}')
    #     name = f'bot{i}'
    #     try:
    #         cl = TGClient(name, api_id, api_hash, bot_tokens[i])
    #     except Exception:
    #         continue

    #     filtered_data, x, f = process_data_columns(df[start:], cl)
    #     print(f'Got {x - prev_x} elements')

    #     filtered_data.to_csv(f'solution4000_{start}.csv', index=False)
    #     start = x
    #     prev_x = x
    #     if f:
    #         break

    files = os.listdir()
    dfs = []
    for file in files:
        if file.startswith('solution4000_') and file.endswith('.csv'):
            d = pd.read_csv(file)
            dfs.append(d)

    final_df = dfs[0] if len(dfs) == 1 else pd.concat(dfs)
    final_df.to_csv('final_solution4000.csv', index=False)
