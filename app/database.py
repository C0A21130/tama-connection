from pymongo import MongoClient

# DBの設定
HOST = "mongo"
PORT = 27017
DB_USER_NAME = "root"
DB_PASSWORD = "password"

# DBに接続
class DataBase:
    def __init__(self):
        self.db = MongoClient(host=HOST, port=PORT, username=DB_USER_NAME, password=DB_PASSWORD)
        self.client = self.db["test_db"]

    def get_collection(self, collection_name:str):
        return self.client[collection_name]
