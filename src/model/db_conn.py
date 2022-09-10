import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.env import setting


def get_env(name) -> str:

    try:
        return os.environ[name]

    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


def get_db_uri() -> str:

    POSTGRES_URL = setting.POSTGRES_URL
    POSTGRES_USER = setting.POSTGRES_USER
    POSTGRES_PASSWORD = setting.POSTGRES_PASSWORD
    POSTGRES_DB = setting.POSTGRES_DB

    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}'

    return DB_URL


engine = create_engine(get_db_uri())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
