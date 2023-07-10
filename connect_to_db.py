from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config("DB")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
localSession = sessionmaker(autocommit=False,autoflush=False,bind=engine)