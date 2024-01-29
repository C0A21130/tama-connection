from sqlalchemy.orm import Session

import model

point_list = ["good", "go", "went"]

class Point():

    # いいねを追加するメソッド
    def increment_status(self, page_id: int, user_id: int, status: str, session: Session):
        # DBから番号が一致する情報を取得する
        points = session.query(model.Points).filter(model.Points.page_id == page_id).all()
        
        # 既に追加されている場合は追加しない
        for point in points:
            if point_list[int(point.point)-1] == status:
                return False
        
        # ポイントを追加する
        try:
            new_point = model.Points(page_id=page_id, user_id=user_id, point=status)
            session.add(new_point)
            session.commit()
        except:
            session.rollback()

    # いいねを取り消すメソッド
    def decrease_status(self, page_id: int, user_id: int, status: str, session: Session) -> bool:
        try:
            session.query(model.Points).filter(model.Points.page_id == page_id, model.Points.user_id == user_id, model.Points.point == status).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return False
