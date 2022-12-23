import time
import requests
import json
import os
import ctypes

SPI_SETDESKWALLPAPER = 20

WALL_URL = "https://loremflickr.com/{width}/{height}/{names}"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
IMAGES_PATH = os.path.join(BASE_DIR, "images")

HEIGHT = 1080
WIDTH = 1980

if not os.path.exists(IMAGES_PATH):
    os.mkdir(IMAGES_PATH)

def load_config():
    with open(CONFIG_PATH) as f:
        return json.loads(f.read())

def get_wall(names):
    names = ",".join(names)
    url = WALL_URL.format(height=HEIGHT, width=WIDTH, names=names)
    print(f"[I] GETTING NEW WALL FROM URL:- {url}")

    resp = requests.get(url)
    if resp.status_code == 200:
        ext = resp.headers.get("Content-Type").split("/")[-1]
        image_path = os.path.join(IMAGES_PATH, f"wall.{ext}")
        print(f"[I] SAVING NEW WALL IMAGE TO PATH:- {image_path}")

        with open(image_path, "wb") as img:
            img.write(resp.content)
            return image_path

def set_wall(image_path):
    print(f"[I] SETTING NEW WALL FROM PATH:- {image_path}")
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def main():
    settings = load_config()
    names = settings["names"]
    change_time = settings["change_time"]

    while True:
        image_path = get_wall(names)
        set_wall(image_path)
        print(f"[I] SLEEPING FOR {change_time} SEC TO SET NEW WALL")
        time.sleep(change_time)

if __name__ == "__main__":
    main()