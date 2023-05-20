from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
    ForeignKey,
    UUID
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_token = Column(UUID, unique=True)
    username = Column(String(40))
    songs = relationship("Song", backref="user", cascade="all, delete-orphan")


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    uuid_key = Column(UUID, unique=True)
    name = Column(String(40))
    song = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("users.id"))
