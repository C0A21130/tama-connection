from database import DataBase

# DBの接続
db = DataBase()
user_data = db.get_collection(collection_name="user_data")

# DBにユーザーを追加する関数
def post_user(user):
    num = user_data.count_documents({})

    user_doc = {
        "user_id" : num + 1,
        "user_name" : user.name,
        "password" : user.password,
        "checked" : []
    }

    user_data.insert_one(user_doc)

    return {"user_id" : num + 1}

# ユーザーの情報を返す関数
def get_user(user_id):
    find = user_data.find_one({"user_id": user_id}, {"_id": False})

    # 返せる情報のみを抜き出して返す
    user_doc = {
        "user_name" : find["user_name"],
        "checked" : find["checked"]
    }

    return user_doc