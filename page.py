import math
from database import DataBase

PER_PAGE_DOCS = 3

class Page:

    @classmethod
    def get_one_page(cls, page_id):
        # DBと接続する
        db = DataBase()
        file_data = db.get_collection(collection_name="file_data")

        # 指定したページ番号から情報を取得する
        search_result: dict = file_data.find_one({"file_name" : page_id}, {"_id" : False})

        return search_result

    def __init__(self):
        self.db = DataBase()
        self.file_data = self.db.get_collection(collection_name="file_data")
    
    # 複数ページを取得する
    def get_pages(self, tag, page_num):
        search_result = []
        max_page = {
            "kankou": self.file_data.count_documents({"tag":"kankou"}), 
            "gurume": self.file_data.count_documents({"tag":"gurume"}),
            "tamasanpo": self.file_data.count_documents({"tag":"tamasanpo"}),
            "omiyage": self.file_data.count_documents({"tag":"omiyage"}),
        }

        # DBに保存されている投稿記事をタグから検索する
        docs = self.file_data.find({"tag" : tag}, {"_id": False})
        finds = list(docs)
        finds_num = len(finds) - 1

        # 投稿記事からページの数とそのページの最後の投稿記事の番号を求める
        end_doc_num = finds_num - (PER_PAGE_DOCS * page_num)

        # 投稿記事を取り出す
        for i in range(end_doc_num, end_doc_num-PER_PAGE_DOCS, -1):
            if (i > -1):
                doc = finds[i]
                search_result.append(doc)

        return {"result":search_result, "max":max_page}

    def post_page(self, page, user_id: int):
        # DBからデータ数を読み取る
        finds_num:int = self.file_data.count_documents({})
        
        # 新しいページ番号の作成
        next_files_num: int = finds_num + 1

        # 受けとったjsonデータから新しいページを作成する
        new_page = {
            "file_name": next_files_num,
            "title": page.title,
            "tag": page.tag,
            "text": page.text,
            "user": user_id,
            "location": {
                "x": page.location.x,
                "y": page.location.y
            },
            "image" : page.image
        }

        # 新しく作成したデータをDBに追加
        self.file_data.insert_one(new_page)

        return next_files_num