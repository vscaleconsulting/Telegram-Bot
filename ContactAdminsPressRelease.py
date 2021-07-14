from scrapers.functions import *
from config import *

if __name__ == '__main__':
    entries = os.listdir(PATH_CAMPAIGN_LIST)
    enum_dict = dict(enumerate(entries))
    for k, v in enum_dict.items():
        print(f'{k}\t:\t{v}')

    campaign_file = PATH_CAMPAIGN_LIST + enum_dict[int(input('Index: '))]

    update_active_numbers('session_ids.csv')

    with open('session_ids.csv') as f:
        str_sessions_tuple = list()
        lines = f.readlines()
        for line in lines[1:]:
            x = line.split(',')
            str_sessions_tuple.append((x[-2].rstrip(), x[-1].rstrip()))
    ph_dict = dict(str_sessions_tuple)

    df = pd.read_csv(campaign_file)
    sess_strs = []
    for sess in df['session_str'].to_list():
        if not pd.isna(sess):
            sess_strs.append(sess)
    bot_use_count = list()

    for b, s in ph_dict.items():
        bot_use_count.append((b, sess_strs.count(s)))

    bot_use_count.sort(key=lambda x: x[1])
    print(bot_use_count)

    bots = [i[0] for i in bot_use_count]

    n = int(input(f'Number of batches to process max({len(ph_dict)}): '))
    batch_size = int(input('Number of messages per bot max(50): '))

    assert n <= len(ph_dict)
    assert batch_size <= 50

    bot = 0
    break_loop = False
    start = 0

    for i in range(n):
        f = False
        count = 0
        while not f:
            if bot == len(bots):
                break_loop = True
                break
            print(f'Using Bot {bot}')
            number = bots[bot].replace(' ', '')
            session_str = ph_dict[bots[bot]]
            cl = TGClient(StringSession(session_str), api_id, api_hash)
            df, f, start, count = contact_admins(df, cl, start, session_str, batch_size-count)

            if not f:
                bot += 1

        bot += 1
        if break_loop:
            break

    df.to_csv(campaign_file, index=False)

