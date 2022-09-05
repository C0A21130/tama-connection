from database import DataBase

# DBの接続
db = DataBase()
user_data = db.get_collection(collection_name="user_data")

def post_user(user):
    num = user_data.count_documents({})

    user_doc = {
        "user_id" : num + 1,
        "user_name" : user.name,
        "password" : user.password,
        "checked" : []
    }

    user_data.insert_one(user_doc)

    return {"test" : "post_user"}