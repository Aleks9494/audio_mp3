import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}" \
                          f":{os.environ.get('POSTGRES_PASSWORD')}" \
                          f"@db/{os.environ.get('POSTGRES_DB')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session


def get_session() -> Generator[scoped_session, None, None]:
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()