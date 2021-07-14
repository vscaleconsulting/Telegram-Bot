import argparse
from scrapers.functions import *
from scrapers.UIAutomation import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Group from which users have to be added", type=str)
    parser.add_argument("destination", help="Group to which users have to be added", type=str)
    parser.add_argument("--search_wait", help="duration in seconds to wait after searching", nargs='?', default=2.5,
                        type=float)
    args = parser.parse_args()

    with open('session_ids_ui_automated.csv') as f:
        str_sessions_tuple = list()
        lines = f.readlines()
    for line in lines[1:]:
        x = line.split(',')
        str_sessions_tuple.append((x[-2].rstrip(), x[-1].rstrip()))

    clx = TGClient(StringSession(str_sessions_tuple[0][1]), api_id=api_id, api_hash=api_hash)
    group_name = clx.get_entity(args.destination).title

    added_csv = f'{group_name}_added.csv'
    not_added_csv = f'{group_name}_not_added.csv'
    privacy_error_csv = 'privacy_error_list.csv'
    mutual_error_csv = 'mutual_error_list.csv'
    f = False
    for ph, sess_str in str_sessions_tuple[1:]:
        dest_users = [user.username for user in clx.get_users(args.destination)]
        users = get_unique_users(clx, args.source, args.destination, added_csv, not_added_csv, privacy_error_csv,
                                 mutual_error_csv)

        activate_tg_window()
        login(ph, sess_str)
        cl = TGClient(StringSession(sess_str), api_id=api_id, api_hash=api_hash)
        cl.join(args.destination)
        not_added, f = add_users_one_by_one(args.destination, users, added_csv, not_added_csv, privacy_error_csv,
                                            mutual_error_csv, cl, clx, args.search_wait)
        print(not_added)
        if f:
            break
