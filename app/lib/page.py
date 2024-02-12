from typing import List
from sqlalchemy.orm import Session

import model

PAGES_NUM = 3

class Page:
    
    @classmethod
    def convert_page(cls, page: model.Pages, points: List[model.Points]) -> dict:
        result = dict()
        tags = ["kankou", "gurume", "tamasanpo", "omiyage"]
        point_tags = ["good", "go", "went"]
        # オブジェクトから辞書へ変換
        result["page_id"] = page.id
        result["title"] = page.title
        result["tag"] = tags[int(page.tag) - 1]
        result["text"] = page.text
        result["location_name"] = page.location_name
        result["location"] = {
            "x": page.lng,
            "y": page.lat
        }
        result["image"] = page.image
        result["good"] = 0
        result["went"] = 0
        result["go"] = 0

        # ポイントオブジェクトが引数にないときは終了する
        if points == None:
            return result

        # ポイント(goodなど)を要素数を数える
        for point in points:
            if page.id == point.page_id:
                index = point_tags[int(point.point)-1]
                result[index] += 1

        return result

    @classmethod
    def get_one_page(cls, page_id: int, user_id: int, session: Session):
        result = dict()

        # DBから一つのページ情報を取得する
        page = session.query(model.Pages).filter(model.Pages.id == page_id).first()
        # DBから複数のポイントを確認する
        points = session.query(model.Points).filter(model.Points.page_id == page_id).all()
        
        # 情報を変換する  
        result = cls.convert_page(page, None)
        result["user_status"] = list()
        point_tags = ["good", "go", "went"]
        # ポイント(goodなど)を要素数を数える
        for point in points:
            index = point_tags[int(point.point)-1]
            result[index] += 1
            # もしユーザーだったら返却値に追加する
            if point.user_id == user_id:
                result["user_status"].append(index)
        
        return result

    # 複数ページを取得する
    def get_pages(self, tag: str, page_num: int, session: Session) -> dict:
        result = dict()
        kankou = list()
        gurume = list()
        tamasanpo = list()
        omiyage = list()

        # DBから一つのページ情報を取得する
        pages = session.query(model.Pages).all()
        # DBから複数のポイントを確認する
        points = session.query(model.Points).all()

        # 取得したデータを分類する
        for page in pages:
            # オブジェクトを辞書に変換
            result = self.convert_page(page, points)

            if (result["tag"] == "kankou"):
                kankou.append(result)
            elif (result["tag"] == "gurume"):
                gurume.append(result)
            elif (result["tag"] == "tamasanpo"):
                tamasanpo.append(result)
            else:
                omiyage.append(result)

        # タグごとの要素数を数える
        max_page = {
            "kankou": len(kankou), 
            "gurume": len(gurume),
            "tamasanpo": len(tamasanpo),
            "omiyage": len(omiyage),
        }

        # 取得する範囲の最初を決める
        start_index = PAGES_NUM * page_num

        # 結果を返却する
        if (tag == "kankou"):
            kankou.reverse()
            return {"result":kankou[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "gurume"):
            gurume.reverse()
            return {"result":gurume[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "tamasanpo"):
            tamasanpo.reverse()
            return {"result":tamasanpo[start_index : start_index+PAGES_NUM], "max":max_page}
        else:
            omiyage.reverse()
            return {"result":omiyage[start_index : start_index+PAGES_NUM], "max":max_page}

    # ページの投稿
    def post_page(self, page: model.ResponsePage, user_id: int, session: Session) -> dict:
        # 受けとったjsonデータから新しいページを作成する
        new_page = model.Pages(
            title = page.title,
            tag = page.tag,
            text = page.text,
            user_id = user_id,
            image = page.image,
            location_name = page.location_name,
            lng = page.location.x,
            lat = page.location.y
        )

        # 新しく作成したデータをDBに追加
        try:
            session.add(new_page)
            session.flush()
        except:
            session.rollback()
            return False
        finally:
            session.commit()
            return True

    # ページの削除
    def delete_page(self, page_id: int, session: Session):
        try:
            session.query(model.Pages).filter(model.Pages.id == page_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return False
        
