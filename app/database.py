from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

#responsible to establish a connection to db from sqlAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#talk to db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to connect
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='Giulia1996',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB conncetion was succesful")
        break
    except Exception as error:
        print("connection faild")
        print("Error: ", error)
        time.sleep(2)


