import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def create_tables():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                department VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                complaint_text TEXT NOT NULL,
                predicted_department VARCHAR(255),
                predicted_priority VARCHAR(50),
                department_confidence_score FLOAT,
                priority_confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("Tables created successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
