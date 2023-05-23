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


WINDOW_TITLE: str = "崩壊：スターレイル"
CLIENT_ID: str = "1101576946086838365"
VERSION: str = "1.2.0"
WEBSITE: str = "https://download.gattxxa.org/StarRailDiscordRPC/"

cooldown: int = 0
now_playing: bool = False
status_updated: bool = False
timestamp = time.mktime(time.localtime())
client: rpc.WinDiscordIpcClient = rpc.DiscordIpcClient

ini = configparser.ConfigParser()
ini.read('./config.ini', encoding='utf-8')


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def find_window(hwnd, window_title):
    global now_playing

    if window_title in win32gui.GetWindowText(hwnd):
        now_playing = True
        return hwnd


def update_status():
    global cooldown, timestamp, now_playing, status_updated, client

    try: win32gui.EnumWindows(find_window, WINDOW_TITLE)
    except: return
        
    if now_playing and status_updated:
        cooldown -= 1
    
    elif now_playing:
        if not status_updated:
            status_updated = True
            timestamp = time.mktime(time.localtime())
            
        if cooldown < 1:
            cooldown = 300
            client = rpc.DiscordIpcClient.for_platform(CLIENT_ID)
            activity = {
                "timestamps": {
                    "start": timestamp
                },
                "assets": {
                    "large_image": "application",
                    "large_text": "崩壊：スターレイル",
                }
            }

            uid = ini.get('Profile', 'UID')
            character = ini.get('Profile', 'Character')

            if uid: 
                activity["details"] = f"UID:{uid}"
            if character:
                activity["assets"]["small_image"] = f"{character}"

            client.set_activity(activity)
                    
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
                    MenuItem("終了", self.stop_program),
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
