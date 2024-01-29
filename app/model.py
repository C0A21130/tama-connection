import enum

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer, String, Boolean, Float, Enum, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class ResponseLocation(BaseModel):
    x: float
    y: float

# put_page関数の受け取るjsonデータの型
class ResponsePage(BaseModel):
    title: str
    tag: str
    text: str
    location_name : str
    location: ResponseLocation
    image: str

# post_user関数の受け取るjsonデータの型
class ResponseUser(BaseModel):
    name: str
    password: str

class Base(DeclarativeBase):
    pass

class Tag(enum.IntEnum):
    kankou = 1
    gurume = 2
    tamasanpo = 3
    omiyage = 4

class Point(enum.IntEnum):
    good = 1
    go = 2
    went = 3

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(64))
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
    location_name: Mapped[str] = mapped_column(String(64))
    lng: Mapped[float] = mapped_column(Float)
    lat: Mapped[float] = mapped_column(Float)

class Points(Base):
    __tablename__ = "points"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    page_id: Mapped[int] = mapped_column(Integer, ForeignKey("pages.id"), primary_key=True)
    point = mapped_column(Enum(Point), primary_key=True)
