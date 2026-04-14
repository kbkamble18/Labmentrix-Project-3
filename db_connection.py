from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        print("✅ Database connection successful")
        return engine

    except Exception as e:
        print("❌ Database connection failed:", e)
        return None
