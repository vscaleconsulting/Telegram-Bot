from scrapers.functions import *

if __name__ == '__main__':
    update_active_numbers('session_ids.csv')
    status = pd.read_csv('status.csv')

    with open('session_ids.csv') as f:
        str_sessions_tuple = list()
        lines = f.readlines()
        for line in lines[1:]:
            x = line.split(',')
            str_sessions_tuple.append((x[-2].rstrip(), x[-1].rstrip()))
    ph_dict = dict(str_sessions_tuple)

    nums = []
    for s in status['sender_no'].to_list():
        if pd.isna(s):
            break
        num = [i for i in s.split(';')]
        nums += num
    bot_use_count = list()

    for b in ph_dict.keys():
        bot_use_count.append((b, nums.count(b)))

    bot_use_count.sort(key=lambda x: x[1])
    print(bot_use_count)

    bots = [i[0] for i in bot_use_count]

    n = int(input(f'Number of files to process max({len(ph_dict)}): '))

    assert n <= len(ph_dict)
    bot = 0
    done = 0
    break_loop = False
    for i, row in status.iterrows():
        if row['status']:
            continue
        print(f'Sending messages to admins in {row["file_name"]}')
        done += 1
        csv = row['file_name']
        file = 'splits/' + csv
        start = 0
        f = False
        df = pd.read_csv(file)
        while not f:
            if bot == len(bots):
                break_loop = True
                break
            number = bots[bot].replace(' ', '')
            session_str = ph_dict[bots[bot]]
            cl = TGClient(StringSession(session_str), api_id, api_hash)
            df, f, start, _ = contact_admins(df, cl, start, session_str)
            # f = True
            status['sender_no'].iloc[i] = ('' if pd.isna(row['sender_no']) else row['sender_no'] + ';') + bots[bot]

            if not f:
                bot += 1

        df.to_csv('splits/' + csv, index=False)
        bot += 1
        if break_loop:
            break
        status['status'].iloc[i] = True

        if done == n:
            break
    status.to_csv('status.csv', index=False)
