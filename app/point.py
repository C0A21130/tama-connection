from database import DataBase

class Point():

    def __init__(self):
        self.db = DataBase()
        self.file_data = self.db.get_collection(collection_name="file_data")

    # いいねや追加するメソッド
    def increment_status(self, page_id: int, user_id: int, status: str):
        find = self.file_data.find_one({"page_id": page_id}, {"_id": False})
        # 既に追加されている場合は追加しない
        if page_id in find[status]:
            return "added"
            
        self.file_data.update_one({"page_id": page_id}, {"$push": {status: user_id}})
        return f"{page_id} at {status}"
