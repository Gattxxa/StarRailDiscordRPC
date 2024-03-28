import configparser
import os
from pystray import Icon, MenuItem, Menu
from PIL import Image
import re
import rpc
import schedule
import sys
import threading
import time
import win32gui

WINDOW_TITLES: list[str] = ["崩壊：スターレイル", "Honkai: Star Rail"]
APPLICATION_ID: str = "1101576946086838365"

timer: int = 0
now_playing: bool = False
status_updated: bool = False

timestamp = time.mktime(time.localtime())
client: rpc.WinDiscordIpcClient = rpc.DiscordIpcClient

ini = configparser.ConfigParser()
ini.read("./config.ini", encoding="utf-8")


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def find_window(hwnd, _):
    global now_playing

    if win32gui.GetWindowText(hwnd) in WINDOW_TITLES:
        now_playing = True
        return hwnd


def setup_client(timestamp):
    global client, ini

    ini.read("./config.ini", encoding="utf-8")

    client = rpc.DiscordIpcClient.for_platform(APPLICATION_ID)
    
    activity = {
        "timestamps": {
            "start": timestamp
        },
        "assets": {
            "large_image": "_application",
        }
    }

    uid = ini.get("Profile", "UID")
    username = ini.get("Profile", "Username")
    character = ini.get("Profile", "Character")

    if uid: 
        activity["details"] = f"UID:{uid}"
    if character:
        activity["assets"]["small_image"] = f"{character}"
        if username:
            activity["assets"]["small_text"] = f"{username}"

    try:
        label = ini.get("Profile", "ButtonLabel")
        url = ini.get("Profile", "URL")
        if re.match(r"https?://", url):
            activity["buttons"] = [{"label": label, "url": url}]
    except:
        pass

    client.set_activity(activity)


def update_status():
    global timer, timestamp, now_playing, status_updated, client

    try:
        win32gui.EnumWindows(find_window, None)
    except:
        return
    print(timer)
    if now_playing and status_updated:
        timer -= 1

        if timer < 1:
            timer = 30
            setup_client(timestamp)

    elif now_playing:
        if not status_updated:
            status_updated = True
            timestamp = time.mktime(time.localtime())
                    
    elif status_updated:
        status_updated = False
        timer = 0
        try: client.close()
        except: pass     

    now_playing = False


# .exe
class StarRailDiscordRPC:
    def __init__(self, image):
        self.status = False
        text = "StarRailDiscordRPC.exe"
        icon = Image.open(image)
        menu = Menu(
                    MenuItem(f"Version: {ini.get('Profile', 'Version')}", None),
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


if __name__ == "__main__":
    system = StarRailDiscordRPC(image=resource_path("icon.ico"))
    system.run_program()
