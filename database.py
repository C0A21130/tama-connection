import os
from pymongo import MongoClient

# DBの設定
DB_URL = os.environ["DB_URL"]

# DBに接続
class DataBase:
    def __init__(self):
        self.db = MongoClient(DB_URL)
        self.client = self.db["TamaConnection"]

    def get_collection(self, collection_name:str):
        return self.client[collection_name]
