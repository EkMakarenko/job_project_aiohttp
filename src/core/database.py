# подключение к базе данных
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.constants import DB_URL

engine = create_engine(DB_URL)  # создаем движок (путь)
Base = declarative_base()  # подключение к базе данных

Session = sessionmaker(bind=engine)
session = Session()
