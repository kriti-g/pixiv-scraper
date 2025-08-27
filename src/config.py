import os
import json
from typing import Literal

SIZE_OPTION = Literal["square_medium", "medium", "large", "original"]

class Config:
    def __init__(self):
        self.download_path = "./downloads"
        self.interval = 1
        self.download_size: SIZE_OPTION = "medium"
        self.refresh_token = None
        self.user_id = None

    def load(self, path, for_downloads: bool):
        with(open(path, "r")) as f:
            config = json.load(f)
            self.download_path = config["download_path"]
            self.interval = config["interval"]
            self.download_size = config["download_size"]
            if for_downloads:
                self.fill_refresh_token(config["refresh_token"])
                self.fill_user_id(config["user_id"])
            else:
                self.refresh_token = config["refresh_token"]
                self.user_id = config["user_id"]


    def save(self, path):
        config = {
            "refresh_token": self.refresh_token,
            "download_path": self.download_path,
            "interval": self.interval,
            "download_size": self.download_size,
            "user_id": self.user_id
        }
        with(open(path, "w")) as f:
            json.dump(config, f, indent=4)

    def fill_user_id(self, try_id):
        self.user_id = try_id if try_id and int(try_id) > 0 else self.input_user_id()

    def input_user_id(self) -> str:
        return input("Input bookmark user id: ")

    def fill_refresh_token(self, try_token):
        self.refresh_token = try_token if try_token and len(try_token) > 0 else self.input_refresh_token()

    def input_refresh_token(self) -> str:
        return input("Input refresh token: ")

    def __str__(self):
        config = {
            "refresh_token": self.refresh_token,
            "download_path": self.download_path,
            "interval": self.interval,
            "download_size": self.download_size,
            "user_id": self.user_id
        }
        return str(config)

    def load_and_fill(self, path: str, for_downloads: bool):
        if os.path.exists(path):
            self.load(path, for_downloads)
        else:
            self.input_refresh_token()
            self.input_user_id()
        self.save(path)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)