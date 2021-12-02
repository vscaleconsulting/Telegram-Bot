import pyautogui
from time import sleep
from PIL import ImageGrab
import pytesseract
from pytesseract import Output
from tqdm import tqdm
import pandas as pd
from scrapers import *
from config import *
import re


def click(button):
    """Clicks on UI element

    Args:
        button (String): path to the image of UI element
    """
    btn = pyautogui.locateOnScreen(button, confidence=.7)
    pyautogui.click(pyautogui.center(btn))
    print('Clicked', button)


def activate_tg_window():
    windows = pyautogui.getWindowsWithTitle('Telegram (')
    tg_window = windows[0]

    tg_window.activate()
    tg_window.resizeTo(780, 1010)
    return tg_window


def add_users_one_by_one(peer, users, added_csv, not_added_csv, privacy_error_csv, mutual_error_csv, tgclient,
                         tgclient_ver,
                         wait_to_load_delay=2.5):
    """Add users to Group/Channel one by one

    Args:
        peer (String): Group/Channel name
        users (list): List of usernames
        privacy_error_csv (str): path to csv file
        wait_to_load_delay (float, optional): Wait time after search. Defaults to 2.5.

    Returns:
        list: List of usernames not added
    """
    tg_window = activate_tg_window()
    not_added = list()
    add_count = 0

    for _ in range(10):
        pyautogui.press('Esc')

    pyautogui.typewrite(peer)
    sleep(wait_to_load_delay)
    pyautogui.press('Down')
    pyautogui.press('Enter')
    sleep(0.5)

    for user in tqdm(users):
        print('Trying to add', user)
        sleep(0.5)
        click('scrapers/UIElements/3DotMenuX2.png')
        sleep(0.5)
        click('scrapers/UIElements/AddMembersX2.png')
        sleep(0.5)
        while pyautogui.locateOnScreen('scrapers/UIElements/AddX2.png', confidence=.7) is None:
            sleep(0.2)
        pyautogui.typewrite(user)
        sleep(wait_to_load_delay)
        screen = ImageGrab.grab()
        cap = screen.crop((tg_window.left, tg_window.top, tg_window.right, tg_window.bottom))
        _, _, cap = cap.split()
        data = pytesseract.image_to_data(cap, output_type=Output.DICT)

        try:
            s = '@' + user
            if s not in data['text']:
                s = s.replace('0', 'O')
            i = data['text'].index(s)
            point = tg_window.left + data['left'][i], tg_window.top + data['top'][i]
            pyautogui.click(point)
            click('scrapers/UIElements/AddX2.png')
            try:
                click('scrapers/UIElements/CANCELX2.png')
            except:
                pass
            sleep(0.2)
            try:
                if pyautogui.locateOnScreen('scrapers/UIElements/PrivacyMessage.png', confidence=.7) is not None:
                    with open(privacy_error_csv, 'a') as f:
                        f.write(user + '\n')
                elif pyautogui.locateOnScreen('scrapers/UIElements/MutualMessageX2.png', confidence=.7) is not None:
                    if tgclient.is_restricted():
                        print('Added', add_count, 'users')
                        print('ACCOUNT REPORTED!')
                        return not_added, False
                    else:
                        ret1 = tgclient.send_message(user, 'hello')
                        if type(ret1) is int and ret1 == -1:
                            ret2 = tgclient_ver.send_message(user, 'hello')
                            if type(ret2) is int and ret2 == -1:
                                with open(mutual_error_csv, 'a') as f:
                                    f.write(user + '\n')
                            else:
                                messages = tgclient_ver.get_chat_messages(user, None)
                                tgclient_ver.delete_messages(user, messages)
                                print('Added', add_count, 'users')
                                print('ACCOUNT RESTRICTED!')
                                return not_added, False
                click('scrapers/UIElements/OKX2.png')
            except TypeError:
                add_count += 1
                print(add_count, 'Added', user)
                with open(added_csv, 'a') as f:
                    f.write(user + '\n')
        except:
            print('-' * 50)
            print(data['text'])
            print('-' * 50)
            sleep(0.5)
            click('scrapers/UIElements/CANCELX2.png')
            not_added.append(user)
            with open(not_added_csv, 'a') as f:
                f.write(user + '\n')
    print('Added', add_count, 'users')
    return not_added, True


def login(ph, session_str):
    for _ in range(5):
        pyautogui.press('Esc')
    try:
        click('scrapers/UIElements/HamburgerMenuX2.png')
    except TypeError:
        click('scrapers/UIElements/HamburgerMenuWithDotX2.png')
    sleep(0.5)
    try:
        click('scrapers/UIElements/DownX2.png')
    except TypeError:
        pass
    try:
        click('scrapers/UIElements/AddAccountX2.png')
    except:
        logout()
        sleep(0.5)
        return login(ph, session_str)
    click('scrapers/UIElements/LoginUsingPhoneX2.png')
    for _ in range(3):
        pyautogui.press('backspace')
    pyautogui.typewrite(ph)
    pyautogui.press('enter')
    sleep(0.5)
    if pyautogui.locateOnScreen('scrapers/UIElements/NEXTX2.png', confidence=.7) is not None:
        sleep(4)
        cl = TGClient(StringSession(session_str), api_id, api_hash)
        message = cl.get_chat_messages(777000, 1)[0].message
        code = re.findall('[0-9]+', message)[0]
        pyautogui.typewrite(code)


def logout():
    for _ in range(5):
        pyautogui.press('Esc')
    try:
        click('scrapers/UIElements/HamburgerMenuX2.png')
    except TypeError:
        click('scrapers/UIElements/HamburgerMenuWithDotX2.png')
    sleep(0.5)
    try:
        click('scrapers/UIElements/UpX2.png')
    except TypeError:
        pass
    click('scrapers/UIElements/SettingsX2.png')
    sleep(0.5)
    click('scrapers/UIElements/3DotMenuX2.png')
    sleep(0.5)
    click('scrapers/UIElements/LogoutX2.png')
    sleep(0.5)
    click('scrapers/UIElements/LOG_OUTX2.png')
