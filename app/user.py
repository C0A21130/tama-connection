from database import DataBase

# DBの接続
db = DataBase()
user = db.get_collection(collection_name="user")

def post_user():
    return {"test" : "post_user"}