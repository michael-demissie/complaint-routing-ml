from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.database import get_db_connection
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def row_to_dict(cursor, row):
    return {desc[0]: row[i] for i, desc in enumerate(cursor.description)}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(user: UserCreate):
    role = "reviewer" if user.reviewer else ("operator" if user.department else "customer")
    hashed_password = pwd_context.hash(user.password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, email, hashed_password, role, department)
            VALUES (%s, %s, %s, %s, %s)
        """, (user.name, user.email, hashed_password, role, user.department))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        cursor.close()
        conn.close()
    return {"message": f"{role} registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        db_user = row_to_dict(cursor, row)
        if not verify_password(user.password, db_user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        token = create_access_token({"user_id": db_user["user_id"], "role": db_user["role"]})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()
