import os
import psycopg2


def init_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL,
        department VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # COMPLAINTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        complaint_text TEXT NOT NULL,

        predicted_department VARCHAR(100),
        predicted_priority VARCHAR(50),

        department_confidence_score FLOAT,
        priority_confidence_score FLOAT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Tables created successfully!")