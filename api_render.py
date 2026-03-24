from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from db_render import get_db_connection  # ✅ changed

from jose import jwt, JWTError
from datetime import datetime, timedelta
import joblib

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------
# Helper: convert rows → dict
# -------------------------
def row_to_dict(cursor, row):
    return {desc[0]: row[i] for i, desc in enumerate(cursor.description)}

def rows_to_dicts(cursor, rows):
    return [row_to_dict(cursor, r) for r in rows]

# -------------------------
# MODELS
# -------------------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: Optional[str] = None
    reviewer: Optional[bool] = False

# -------------------------
# REGISTER
# -------------------------
@app.post("/register")
def register(user: UserCreate):
    role = "reviewer" if user.reviewer else ("operator" if user.department else "customer")

    hashed_password = pwd_context.hash(user.password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, hashed_password, role, department)
        VALUES (%s, %s, %s, %s, %s)
    """, (user.name, user.email, hashed_password, role, user.department))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"{role} registered successfully"}

# -------------------------
# AUTH
# -------------------------
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    db_user = row_to_dict(cursor, row)

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({
        "user_id": db_user["user_id"],
        "role": db_user["role"]
    })

    cursor.close()
    conn.close()

    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# LOAD MODELS
# -------------------------
department_model = joblib.load("models/department_model.joblib")
priority_model = joblib.load("models/priority_model.joblib")

def predict_department_and_priority(text: str):
    input_data = [text]

    dept_pred = department_model.predict(input_data)[0]
    dept_conf = max(department_model.predict_proba(input_data)[0])

    prio_pred = priority_model.predict(input_data)[0]
    prio_conf = max(priority_model.predict_proba(input_data)[0])

    return {
        "department": dept_pred,
        "priority": prio_pred,
        "department_confidence": float(dept_conf),
        "priority_confidence": float(prio_conf)
    }

# -------------------------
# AUTH DEPENDENCY
# -------------------------
security = HTTPBearer()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row_to_dict(cursor, row) if row else None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_user_by_id(payload.get("user_id"))

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# CUSTOMER
# -------------------------
@app.get("/my-complaints")
def get_my_complaints(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT complaint_text, predicted_department, predicted_priority,
               department_confidence_score, priority_confidence_score, created_at
        FROM complaints
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (current_user["user_id"],))

    complaints = rows_to_dicts(cursor, cursor.fetchall())

    cursor.close()
    conn.close()

    return complaints

# -------------------------
# SUBMIT
# -------------------------
class ComplaintCreate(BaseModel):
    complaint_text: str

@app.post("/submit-complaint")
def submit_complaint(complaint: ComplaintCreate, current_user = Depends(get_current_user)):
    prediction = predict_department_and_priority(complaint.complaint_text)

    dept = prediction["department"]
    prio = prediction["priority"]
    dept_conf = prediction["department_confidence"]
    prio_conf = prediction["priority_confidence"]

    if dept_conf < 0.5:
        dept = None
    if prio_conf < 0.5:
        prio = None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (
            user_id, complaint_text, predicted_department,
            predicted_priority, department_confidence_score, priority_confidence_score
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (current_user["user_id"], complaint.complaint_text, dept, prio, dept_conf, prio_conf))

    conn.commit()
    cursor.close()
    conn.close()

    return {"department": dept, "priority": prio}