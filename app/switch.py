from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, Integer, String, Boolean, Float, Enum, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

import enum

# MongoDB
db = MongoClient(host="mongo", port=27017, username="root", password="password")
client = db["TamaConnection"]
file_data = client["file_data"]
user_data = client["user_data"]

# ORM(MySQL)
DB_URL = "mysql+pymysql://root:root@db:3306/tama_connection?charset=utf8"
engine = create_engine(DB_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Tag(enum.IntEnum):
    kankou = enum.auto()
    gurume = enum.auto()
    tamasanpo = enum.auto()
    omiyage = enum.auto()

class Point(enum.IntEnum):
    good = enum.auto()
    go = enum.auto()
    went = enum.auto()

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(512))
    admin: Mapped[bool] = mapped_column(Boolean)
    taxi: Mapped[bool] = mapped_column(Boolean)

class Pages(Base):
    __tablename__ = "pages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32))
    tag = mapped_column(Enum(Tag))
    text: Mapped[str] = mapped_column(String(512))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    image: Mapped[str] = mapped_column(Text)
    location_name: Mapped[str] = mapped_column(String(32))
    lng: Mapped[float] = mapped_column(Float)
    lat: Mapped[float] = mapped_column(Float)

class Points(Base):
    __tablename__ = "points"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    page_id: Mapped[int] = mapped_column(Integer, ForeignKey("pages.id"), primary_key=True)
    point = mapped_column(Enum(Point), primary_key=True)

session = Session()
print("start")
try:
    # yield session
    result = user_data.find({}, {"_id": False})
    for doc in list(result):
        user = Users()
        user.id=int(doc["id"])
        user.name=str(doc["name"])
        user.password=str(doc["password"])
        user.taxi = False
        try:
            doc["admin"]
            user.admin=True
        except:
            user.admin=False
    # user = Users(id=0, name="test", password="afa", admin=False, taxi=False)
        session.add(user)
        session.flush()
    print("first commit")
    session.commit()

    result = file_data.find({}, {"_id": False})
    for doc in list(result):
        page = Pages(id=doc["page_id"], title=doc["title"], tag=doc["tag"], text=doc["text"], user_id=doc["user"], image=doc["image"], location_name=doc["location_name"], lng=doc["location"]["x"], lat=doc["location"]["y"])
        session.add(page)
        session.flush()
        for i, status in enumerate(["good", "go", "went"]):
            for p in doc[status]:
                point = Points(page_id=doc["page_id"], user_id=p, point=(i+1))
                session.add(point)
                session.flush()
    print("second commit")
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

print("end")