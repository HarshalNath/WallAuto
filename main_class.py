import os
import time
import json
import ctypes
import requests

SPI_SETDESKWALLPAPER = 20

WALL_URL = "https://loremflickr.com/{width}/{height}/{names}"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
IMAGES_PATH = os.path.join(BASE_DIR, "images")

HEIGHT = 1080
WIDTH = 1980

if not os.path.exists(IMAGES_PATH):
    os.mkdir(IMAGES_PATH)

class Wall():

    def load_config(self):
        with open(CONFIG_PATH) as f:
            return json.loads(f.read())

    def get_wall(self):
        names = ",".join(self.names)
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

    def set_wall(self):
        print(f"[I] SETTING NEW WALL FROM PATH:- {self.image_path}")
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.image_path, 3)

    def main(self):
        settings = self.load_config()
        self.names = settings["names"]
        self.change_time = settings["change_time"]

        while True:
            self.image_path = self.get_wall()
            if self.image_path is not None:
                self.set_wall()
                print(f"[I] SLEEPING FOR {self.change_time} SEC TO SET NEW WALL")
                time.sleep(self.change_time)

if __name__ == "__main__":
    wall = Wall()
    wall.main()