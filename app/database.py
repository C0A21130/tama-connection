import os
from pymongo import MongoClient

# DBの設定
DB_URL = os.environ["DB_URL"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER_NAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

# DBに接続
class DataBase:
    def __init__(self):
        self.db = MongoClient(DB_URL)
        self.client = self.db["TamaConnection"]

    def get_collection(self, collection_name:str):
        return self.client[collection_name]
