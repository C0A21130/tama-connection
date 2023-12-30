from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, Integer, String, Boolean, Float, Enum, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

import enum
import os

# MongoDB
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
db = MongoClient(host=DB_HOST, port=int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)
client = db["TamaConnection"]
file_data = client["file_data"]
user_data = client["user_data"]

# ORM(MySQL)
DB_URL = "mysql+pymysql://root:root@db:3306/tama_connection?charset=utf8"
engine = create_engine(DB_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Tag(enum.Enum):
    kankou = 1
    gurume = 2
    tamasanpo = 3
    omiyage = 4

class Point(enum.Enum):
    good = 1
    go = 2
    went = 3

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(512))
    admin: Mapped[bool] = mapped_column(Boolean)
    taxi: Mapped[bool] = mapped_column(Boolean)

class Locations(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("pages.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    lng: Mapped[float] = mapped_column(Float)
    lat: Mapped[float] = mapped_column(Float)

class Pages(Base):
    __tablename__ = "pages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32))
    tag = mapped_column(Enum(Tag))
    text: Mapped[str] = mapped_column(String(512))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    image: Mapped[str] = mapped_column(Text)

class Points(Base):
    __tablename__ = "points"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    page_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    point = mapped_column(Enum(Point))


session = Session()
print("test")
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
    session.commit()

    result = file_data.find({}, {"_id": False})
    for doc in list(result):
        page = Pages(id=doc["page_id"], title=doc["title"], tag=doc["tag"], text=doc["text"], user_id=doc["user"], location_id=doc["page_id"], image=doc["image"])
        location = Locations(id=doc["page_id"], name=doc["location_name"], lng=doc["location"]["x"], lat=doc["location"]["y"])
        session.add(page)
        session.flush()
        session.add(location)
        session.flush()
        for status in ["good", "go", "went"]:
            for d in doc[status]:
                point = Points(user_id=d, page_id=doc["page_id"], point="good")
                session.add(point)
                session.flush()
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
