from pymongo import MongoClient

# DBの設定
HOST = "mongo"
PORT = 27017
USER_NAME = "root"
PASSWORD = "password"

# DBに接続
class DataBase:
    def __init__(self):
        self.db = MongoClient(host="mongo", port=27017, username="root", password="password")
        self.client = self.db["test_db"]

    def search_tags(self):
        return self.client["search_tags"]

    def search_locations(self):
        return self.client["search_locations"]

    def file_data(self):
        return self.client["file_data"]
