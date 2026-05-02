import os
import psycopg2
from dotenv import load_dotenv
from app.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            sslmode="require"
        )
        return conn
    except Exception as e:
        logger.error("Database connection failed: %s", str(e))
        raise
