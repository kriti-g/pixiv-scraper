import json
from typing import Literal

SIZE_OPTION = Literal["square_medium", "medium", "large", "original"]

class Config:
    def __init__(self):
        self.refresh_token = ""
        self.download_path = "./downloads"
        self.interval = 1
        self.download_size: SIZE_OPTION = "medium"
        self.user_id: 0

    def load(self, path):
        with(open(path, "r")) as f:
            config = json.load(f)
            self.refresh_token = config["refresh_token"]
            self.download_path = config["download_path"]
            self.interval = config["interval"]
            self.download_size = config["download_size"]
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

    def input_user_id(self):
        self.user_id = input("Input bookmark user id: ")

    def input_refresh_token(self):
        self.refresh_token = input("Input refresh token: ")

    def __str__(self):
        config = {
            "refresh_token": self.refresh_token,
            "download_path": self.download_path,
            "interval": self.interval,
            "download_size": self.download_size,
            "user_id": self.user_id
        }
        return str(config)