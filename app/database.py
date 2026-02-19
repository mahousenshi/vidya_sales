from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Carrega o .env
load_dotenv()

# Configuração postgresql
POSTGRESQL_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://usuario:senha@localhost:5432/vidya_db"
)

engine = create_engine(POSTGRESQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuração mongodb
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password@localhost:27017/")

mongo_client = MongoClient(MONGO_URL)
db = mongo_client.get_database("vidya_analytics")
nosql_db = db.comments

# Garante que o banco abra e feche corretamente em cada chamada da API
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
