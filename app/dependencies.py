from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.database import get_db_connection
from app.config import SECRET_KEY, ALGORITHM
from app.logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()

def row_to_dict(cursor, row):
    return {desc[0]: row[i] for i, desc in enumerate(cursor.description)}

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return row_to_dict(cursor, row)
    finally:
        cursor.close()
        conn.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_user_by_id(payload.get("user_id"))
        if not user:
            logger.warning("Token valid but user not found | user_id=%s", payload.get("user_id"))
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        logger.warning("Invalid token attempt")
        raise HTTPException(status_code=401, detail="Invalid token")
