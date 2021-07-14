from scrapers.clients import *
from scrapers.functions import *
from config import *
from constants import *

start = 0
prev_x = 0

try:
    os.mkdir(PATH_ADMIN_LIST)
except:
    pass

entries = os.listdir(PATH_TELEGRAM_PRESS_RELEASE)
enum_dict = dict(enumerate(entries))
for k, v in enum_dict.items():
    print(f'{k}\t:\t{v}')

d_indices = set(map(int, input('Indices: ').split()))

for d_index in d_indices:
    assert d_index in enum_dict.keys()

for d_index in d_indices:
    f = enum_dict[d_index]
    print(f'Processing {f}')
    csv = os.path.join(PATH_TELEGRAM_PRESS_RELEASE, f)
    df = pd.read_csv(csv)
    site = f.split()[-1].split('.')[0]
    adminlist_file = PATH_ADMIN_LIST + f'Adminlist_{site}.csv'

    try:
        cdf = pd.read_csv(adminlist_file)
        end = df.index[df['title_of_press_release'] == cdf['title_of_press_release'].iloc[0]][0]
        df = df[:end]
    except:
        cdf = pd.DataFrame()

    for i, token in enumerate(bot_tokens):
        print(f'Using Bot {i}')
        name = f'bot{i}'
        cl = TGClient(name, api_id, api_hash, bot_tokens[i])

        filtered_data, x, f = process_tg_links(df[start:], cl, additional_cols=['name_of_project', 'title_of_press_release'])
        # print(f'Got {x - prev_x} elements')

        filtered_data.to_csv(f's_{start}.csv', index=False)
        start = x
        prev_x = x
        if f:
            break

    files = os.listdir()
    dfs = list()
    for f in files:
        if f.startswith('s_') and f.endswith('.csv'):
            d = pd.read_csv(f)
            os.remove(f)
            dfs.append(d)

    if len(dfs) == 1:
        final_df = dfs[0]
    else:
        final_df = pd.concat(dfs)
    final_df = pd.concat([final_df, cdf])
    final_df.to_csv(adminlist_file, index=False)
