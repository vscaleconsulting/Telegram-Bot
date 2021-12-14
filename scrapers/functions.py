import json
import os
import re
import numpy as np
import pandas as pd
import requests
from telethon.errors.rpcerrorlist import UserBotError, PeerFloodError
from telethon.tl.types import User, Channel, UserStatusOnline, UserStatusRecently
from telethon.sessions import StringSession
from tqdm import tqdm
from random import randint
from config import *
from scrapers.clients import *
from multiprocessing import Process, Manager
from telethon.tl.patched import Message


def get_data(start=1, limit=5000, batch_size=900,__json=False):
    """Get Crptocoin Data

    Args:
        start (int, optional): Sets the start value of the requried data. Defaults to 1.
        limit (int, optional): Limit for the amount of data. Defaults to 5000.
        batch_size (int, optional): Batch size for every iteration. Defaults to 900.

    Returns:
        DataFrame: Returns a DataFrame Object
    """
    if batch_size > 950 or start < 1 or limit > 5000:
        raise ValueError

    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start={start}&limit={limit}&convert=USD&CMC_PRO_API_KEY=b85e274a-623a-4630-8703-7a10dc7533a9"
    headers = {
        'Cookie': '__cfduid=d80d94e8b91c6e501ef97b018900ee5161618654054'
    }
    response = requests.request("GET", url, headers=headers, data={})

    assert response.status_code == 200

    data = json.loads(response.text)
    df = pd.DataFrame(data=data['data'])
    ids = df['id'].tolist()

    size = batch_size
    max_size = len(ids) + size
    initial_size = 0
    dfs = []

    while size < max_size:
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?CMC_PRO_API_KEY={PRO_API_KEY}&id={','.join(list(map(str, ids[initial_size:size])))}"

        response = requests.request("GET", url, headers=headers, data={})
        initial_size += batch_size
        size += batch_size

        data = json.loads(response.text)
        if(__json):
            return data
        data = pd.DataFrame(data=data['data'])
        data = data.transpose()

        dfs.append(data.copy())

    ret = pd.concat(dfs, ignore_index=True)
    return ret


def process_data_columns(df, tg_client):
    """Process Data Column Wise

    Args:
        df (DataFrame): DataFrame from which to process the data
        tg_client (TGClient): TGClient to use

    Returns:
        Dataframe, Int, Boolean: Processed DataFrame, Number of Iterations, Whether the loop was broked because of FloodError
    """
    # New dataframe to store the extracted data from the URLs column
    df0 = pd.DataFrame(columns=['id', 'name', 'symbol', 'description', 'website', 'telegram_1', 'telegram_2',
                                'discord', 'twitter', 'reddit', 'telegram_1_name', 'telegram_1_is_group',
                                'telegram_2_name', 'telegram_2_is_group'])

    request_count = 0
    column_count = 0
    break_loop = False
    i = 0
    for i, row in tqdm(df.iterrows()):  # Iterate through the URLs
        if break_loop:
            print(f'index: {i}  id: {row["id"]}')
            break

        d = dict()
        d['id'] = row['id']
        d['name'] = row['name']
        d['symbol'] = row['symbol']
        d['description'] = row['description']
        urls = row['urls']

        # Assign values to the keys if value exists
        for key in ['website', 'twitter', 'reddit']:
            if len(urls[key]) != 0:
                d[key] = urls[key][0]

        tg_ = True  # Variable to switch between the 2 columns of telegram links

        # Search for the substrings and save links if match is found
        # (Multiple substrings to cover all the cases and ignore false positives)
        admin_ids = list()
        admin_count = 0
        for link in urls['chat']:
            if 'discord.' in link or 'discordapp.com/' in link or link.endswith('/discord'):
                d['discord'] = link
                continue
            entity = tg_client.get_entity(link)
            # if 't.me/' in link or 'telegram.me/' in link or '/telegram' in link:
            if entity == -2:
                break_loop = True
                break
            if type(entity) != int:
                request_count += 1
                if type(entity) == Channel:
                    if tg_:
                        tg_ = False
                        d['telegram_1_name'] = entity.title
                        d['telegram_1'] = link
                        d['telegram_1_is_group'] = not entity.broadcast
                    else:
                        d['telegram_2_name'] = entity.title
                        d['telegram_2'] = link
                        d['telegram_2_is_group'] = not entity.broadcast

                if type(entity) == Channel and not entity.broadcast or type(entity) == User:
                    request_count += 1
                    admins = tg_client.get_admins(entity)
                    if admins == -2:
                        break_loop = True
                        break
                    for admin in admins:
                        if not admin.bot and admin.username is not None and admin.id not in admin_ids:
                            admin_count += 1
                            admin_ids.append(admin.username)
                            if column_count < admin_count:
                                column_count += 1
                                df0[f'tg admin {admin_count} name'] = np.nan
                                df0[f'tg admin {admin_count} username'] = np.nan
                                df0[f'tg admin {admin_count} contact url'] = np.nan
                                df0[f'tg admin {admin_count} status'] = np.nan

                            d[f'tg admin {admin_count} name'] = admin.first_name + (
                                ' ' + admin.last_name if admin.last_name is not None else '')
                            d[f'tg admin {admin_count} username'] = admin.username
                            d[f'tg admin {admin_count} contact url'] = 'https://t.me/' + admin.username
                            d[f'tg admin {admin_count} status'] = admin.status

        # Append row to dataframe
        if admin_count == 0:
            continue
        df0 = df0.append(d, ignore_index=True)

    return df0, i - 1, not break_loop


def process_tg_links(df, tg_client, additional_cols=[]):
    column_count = 0
    break_loop = False
    i = 0
    df0 = pd.DataFrame(columns=additional_cols + ['telegram_1', 'telegram_1_name', 'telegram_1_is_group'])
    for i, row in tqdm(df.iterrows()):
        if break_loop:
            print(f'index: {i}  id: {row["id"]}')
            break
        d = dict()
        for col in additional_cols:
            d[col] = row[col]

        admin_count = 0
        entity = tg_client.get_entity(row['telegram'])
        if type(entity) is int and entity == -2:
            break_loop = True
            break
        if type(entity) == Channel and not entity.broadcast:
            d['telegram_1_is_group'] = True
            d['telegram_1'] = row['telegram']
            d['telegram_1_name'] = entity.title

            admins = tg_client.get_admins(entity)
            if type(admins) is int and admins == -2:
                break_loop = True
                break
            for admin in admins:
                if not admin.bot and admin.username is not None:
                    admin_count += 1
                    if column_count < admin_count:
                        column_count += 1
                        df0[f'tg admin {admin_count} name'] = np.nan
                        df0[f'tg admin {admin_count} username'] = np.nan
                        df0[f'tg admin {admin_count} contact url'] = np.nan
                        df0[f'tg admin {admin_count} status'] = np.nan

                    d[f'tg admin {admin_count} name'] = admin.first_name + (
                        ' ' + admin.last_name if admin.last_name is not None else '')
                    d[f'tg admin {admin_count} username'] = admin.username
                    d[f'tg admin {admin_count} contact url'] = 'https://t.me/' + admin.username
                    d[f'tg admin {admin_count} status'] = admin.status
        if admin_count == 0:
            continue
        df0 = df0.append(d, ignore_index=True)
    return df0, max(i - 1, 0), not break_loop


def contact_admins(df, tg_client, start, session, max_count=None):
    """Message the Admins

    Args:
        df (DataFrame): DataFrame to use
        tg_client (TGClient): TGClient to use
        start (int): start index n df
        session (str): session string

    Returns:
        (DataFrame, bool, int): processed DataFrame, False if FloodWaitError exception was raised, index at which FloodWaitError exception was raised
    """
    sent = 0
    for i, row in tqdm(df.iterrows()):
        if max_count is not None and max_count == sent:
            break
        if i < start:
            continue
        if not row['delivered']:
            sent += 1
            url = row['admin_contact_url']
            message = row['opening_message']
            status = tg_client.send_message(url, message)
            if type(status) == int and status == -2:
                return df, False, i, sent - 1
            elif type(status) == int and status == -1:
                print("Error while sending message")
            else:
                df['delivered'].iloc[i] = True
                df['session_str'].iloc[i] = session
    return df, True, 0, sent


def generate_messages(df, message, max_admins=None, additional_cols=[]):
    """Generate messages

    Args:
        df (DataFrame): DataFrame to use
        message (str): Message to send
        max_admins (int, optional): Maximum number of admins to process per group. Defaults to None.

    Returns:
        DataFrame: Processed DataFrame
    """
    ret_df = pd.DataFrame(columns=additional_cols + ['telegram_chat',
                                                     'admin_name', 'admin_contact_url', 'opening_message', 'delivered',
                                                     'replied',
                                                     'session_str', 'reply'])
    end = sum([i.endswith('status') for i in df.columns])
    if max_admins is not None:
        end = min(max_admins + 1, end)
    for _, row in tqdm(df.iterrows()):
        for i in range(1, end):
            status = row[f'tg admin {i} status']
            if not (type(status) == str and status in ['UserStatusRecently()', 'UserStatusOnline()']):
                continue
            url = row[f'tg admin {i} contact url']
            if pd.isna(url):
                break
            admin_name = row[f'tg admin {i} name']
            cols = re.findall('\<([^>]+)\>', message)

            if row['telegram_1_is_group']:
                chat = row['telegram_1']
            elif row['telegram_2_is_group']:
                chat = row['telegram_2']
            else:
                chat = np.nan

            mess = message.replace('<tg admin name>', admin_name)
            for col in cols:
                if col == 'tg admin name':
                    continue
                mess = mess.replace('<' + col + '>', row[col])

            matches = re.findall('\{([^}]+)\}', message)

            for match in matches:
                l = [i.strip() for i in match.split('|')]
                mess = mess.replace('{' + match + '}', l[randint(0, len(l) - 1)])

            d = {'telegram_chat': chat, 'admin_name': admin_name, 'admin_contact_url': url, 'opening_message': mess,
                 'delivered': False, 'replied': False}

            for col in additional_cols:
                d[col] = row[col]

            ret_df = ret_df.append(d, ignore_index=True)

    return ret_df


def split_csv(csv, start, lines, num_files=None, dest=''):
    """Splits the csv

    Args:
        csv (str): path of the csv file
        start (int): line number in csv file
        lines (int): number of lines per split file
        num_files (int, optional): max number of files to generate. Defaults to None.
        dest (str, optional): path of the destination folder. Defaults to ''.
    """
    csv_data = pd.DataFrame(columns=['file_name', 'status', 'sender_no'])
    df = pd.read_csv(csv)
    if dest == '':
        x = sorted(os.listdir())
    else:
        x = sorted(os.listdir(dest[:-1]))
    xi = list()
    for i in x:
        xi.append(int(i.split('_')[-1].split('.')[0]))
    if len(xi) == 0:
        x = 0
    else:
        x = max(xi)
    j = 1
    while start < df.shape[0]:
        d = df[start:start + lines]
        name = f'{csv[:-4]}_split_{j + x}.csv'
        d.to_csv(dest + name, index=False)
        csv_data = csv_data.append({'file_name': name, 'status': False}, ignore_index=True)
        j += 1
        start += lines
        if num_files is not None and j > num_files:
            break
    print(f'Generated {j - 1} files')
    csv_data.to_csv('status.csv', index=False)


def check(ph_dict, ret):
    """Helper function for update_active_numbers function

    Args:
        ph_dict (dict): dict {<phone>: <session str>}
        ret (bool): True if phone number is active else False
    """
    for ph, sid in ph_dict.items():
        try:
            tg_client = TGClient(StringSession(sid), api_id=api_id, api_hash=api_hash)
            tg_client.connect()
            ret[ph] = True
        except:
            ret[ph] = False


def update_active_numbers(csv):
    """Update the csv with only the working phone numbers

    Args:
        csv (str): path to the csv file

    Returns:
        DataFrame: processed DataFrame
    """
    with open(csv) as f:
        str_sessions_tuple = list()
        lines = f.readlines()
        for line in lines[1:]:
            x = line.split(',')
            str_sessions_tuple.append((x[-2].rstrip(), x[-1].rstrip()))
        ph_dict = dict(str_sessions_tuple)

    manager = Manager()
    ret = manager.dict()
    th = Process(target=check, args=(ph_dict, ret,))
    th.start()
    th.join()

    df = pd.DataFrame(columns=['number', 'client_session'])
    for ph, status in ret.items():
        if status:
            df = df.append({'number': ph, 'client_session': ph_dict[ph]}, ignore_index=True)

    df.to_csv(csv, index=False)
    return df


def add_users_to_channel(tgclient, users, channel, include_bots=False):
    """Add users to channel

    Args:
        tgclient (TGClient): TGClient to use
        users (list): list of users
        channel (str): channel link
        include_bots (bool, optional): Set True to include bots. Defaults to False.

    Returns:
        (bool, list): True if all users were processed, list of users who have privacy settings enabled
    """
    current_users = tgclient.get_users(channel)
    queue = [user for user in users if user not in current_users]
    done = list()
    privacy_error = list()

    for user in tqdm(queue):
        ret = tgclient.invite_to_channel(channel, [user])
        print(ret)
        # sleep(15)
        if type(ret) is int:
            if ret == -4 and include_bots:
                tgclient.update_admin_rights(channel, user, change_info=True,
                                             post_messages=True,
                                             edit_messages=True,
                                             delete_messages=True,
                                             ban_users=True,
                                             invite_users=True,
                                             pin_messages=True,
                                             add_admins=True,
                                             anonymous=True,
                                             manage_call=True,
                                             other=True)
            elif ret == -3:
                print('PeerFloodError')
                sleep(15 * 60)
            elif ret in [-5, -6]:
                print('Privacy restricted error')
                privacy_error.append(user)
        else:
            done.append(user)
            # print('User added:', user.username)

    current_users = tgclient.get_users(channel)
    new_queue = [user for user in queue if user not in (current_users + privacy_error)]

    return len(new_queue) == 0, privacy_error


def forward_new_messages(tgclient, source, destination, pin_latest=False):
    """Forward messages from source to destination which are not in destination

    Args:
        tgclient (TGClient): Telegram client to use
        source (str): source channel link
        destination (str): destination channel link
        pin_latest (bool, optional): set true to pin latest message. Defaults to False.
    """
    sent = [me.fwd_from.channel_post for me in tgclient.get_chat_messages(destination, None) if type(me) is Message]
    forwards = [me for me in tgclient.get_chat_messages(source, None) if type(me) is Message and me.id not in sent]
    tgclient.forward_messages(destination, forwards)
    if pin_latest:
        latest_id = tgclient.get_chat_messages(destination, None)[0].id
        tgclient.pin_message(destination, latest_id)


def get_unique_users(tgclient, source, destination, added_csv, not_added_csv, privacy_error_csv, mutual_error_csv):
    """Get list of users in source who are not in destinantion

    Args:
        tgclient (TGClient): Telegram client to use
        source (str): source channel link
        destination (str): destination channel link
        privacy_error_csv (str): path to csv file

    Returns:
        list: list of users
    """
    dest_users = [user.username for user in tgclient.get_users(destination)]
    try:
        with open(privacy_error_csv, 'r') as f:
            priv_error = list(set(f.readlines()))
        with open(privacy_error_csv, 'w') as f:
            f.writelines(priv_error)
        priv_error = [i.strip('\n') for i in priv_error]
    except:
        priv_error = []
    try:
        with open(added_csv, 'r') as f:
            added = list(set(f.readlines()))
        with open(added_csv, 'w') as f:
            f.writelines(added)
        added = [i.strip('\n') for i in added]
    except:
        added = []
    try:
        with open(not_added_csv, 'r') as f:
            not_added = list(set(f.readlines()))
        with open(not_added_csv, 'w') as f:
            f.writelines(not_added)
        not_added = [i.strip('\n') for i in not_added]
    except:
        not_added = []
    try:
        with open(mutual_error_csv, 'r') as f:
            mutual_error = list(set(f.readlines()))
        with open(mutual_error_csv, 'w') as f:
            f.writelines(mutual_error)
        mutual_error = [i.strip('\n') for i in mutual_error]
    except:
        mutual_error = []
    users = [user.username for user in tgclient.get_users(source) if
             not user.bot and user.username is not None and type(
                 user.status) in (UserStatusRecently, UserStatusOnline) and user.username not in (
                     dest_users + priv_error + added + not_added + mutual_error)]

    return users


def get_admin_usernames(group_link, tgclient, csv='admins.csv', fetch_new=False):
    try:
        df = pd.read_csv(csv, converters={'admins_list': eval})
    except Exception as e:
        print(e)
        df = pd.DataFrame(columns=['group_link', 'admins_list'])

    i = df.loc[df['group_link'] == group_link]
    if i.shape[0] > 0 and not fetch_new:
        return i['admins_list'].iloc[0]

    admin_unames = [admin.username for admin in tgclient.get_admins(group_link)]
    df = df[df.group_link != group_link]
    df = df.append({'group_link': group_link, 'admins_list': admin_unames}, ignore_index=True)
    df.to_csv(csv, index=False)
    return admin_unames


