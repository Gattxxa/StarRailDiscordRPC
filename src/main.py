import configparser
import os
from pystray import Icon, MenuItem, Menu
from PIL import Image
import rpc
import schedule
import sys
import threading
import time
import webbrowser
import win32gui


WINDOW_TITLE_ENG: str = "Honkai: Star Rail"
CLIENT_ID_ENG: str = "1110781234793160735"

WINDOW_TITLE_JP: str = "崩壊：スターレイル"
CLIENT_ID_JP: str = "1101576946086838365"

VERSION: str = "1.2.1"
WEBSITE: str = "https://download.gattxxa.org/StarRailDiscordRPC/"

cooldown: int = 0
now_playing: bool = False
language: str = "en-us"
status_updated: bool = False
timestamp = time.mktime(time.localtime())
client: rpc.WinDiscordIpcClient = rpc.DiscordIpcClient

ini = configparser.ConfigParser()
ini.read('./config.ini', encoding='utf-8')


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def find_window(hwnd, _):
    global now_playing, language
    
    if WINDOW_TITLE_ENG in win32gui.GetWindowText(hwnd):
        now_playing = True
        language = "en-us"
        return hwnd
    
    if WINDOW_TITLE_JP in win32gui.GetWindowText(hwnd):
        now_playing = True
        language = "ja-jp"
        return hwnd


def setup_client(timestamp):
    global client 

    if language == "ja-jp":
        window_title = WINDOW_TITLE_JP
        client_id = CLIENT_ID_JP
    else:
        window_title = WINDOW_TITLE_ENG
        client_id = CLIENT_ID_ENG

    client = rpc.DiscordIpcClient.for_platform(client_id)
    activity = {
        "timestamps": {
            "start": timestamp
        },
        "assets": {
            "large_image": "application",
            "large_text": f"{window_title}",
        }
    }

    uid = ini.get('Profile', 'UID')
    character = ini.get('Profile', 'Character')

    if uid: 
        activity["details"] = f"UID:{uid}"
    if character:
        activity["assets"]["small_image"] = f"{character}"

    client.set_activity(activity)


def update_status():
    global cooldown, timestamp, now_playing, status_updated, client

    try: win32gui.EnumWindows(find_window, None)
    except: return
        
    if now_playing and status_updated:
        cooldown -= 1
    
    elif now_playing:
        if not status_updated:
            status_updated = True
            timestamp = time.mktime(time.localtime())
            
        if cooldown < 1:
            cooldown = 300
            setup_client(timestamp)
                
    elif status_updated:
        status_updated = False
        cooldown = 0
        try: client.close()
        except: pass     

    now_playing = False


class StarRailDiscordRPC:
    def __init__(self, image):
        self.status = False
        text = "StarRailDiscordRPC.exe"
        icon = Image.open(image)
        menu = Menu(
                    MenuItem(f"Version {VERSION}", self.open_website),
                    MenuItem("Exit", self.stop_program),
                )
        self.icon = Icon(name=text, title=text, icon=icon, menu=menu)

    def run_schedule(self):
        schedule.every(1).seconds.do(update_status)
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def run_program(self):
        self.status = True
        task_thread = threading.Thread(target=self.run_schedule)
        task_thread.start()
        self.icon.run()
    
    def stop_program(self):
        self.status = False
        self.icon.stop()

    def open_website(self):
        webbrowser.open(WEBSITE)


if __name__ == "__main__":
    system = StarRailDiscordRPC(image=resource_path("icon.ico"))
    system.run_program()
