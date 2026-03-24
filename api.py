from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from db import get_db_connection

from jose import jwt, JWTError
from datetime import datetime, timedelta

import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base model (single input model for all roles)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: Optional[str] = None
    reviewer: Optional[bool] = False


@app.post("/register")
def register(user: UserCreate):
    # determine role
    if user.reviewer:
        role = "reviewer"
    elif user.department:
        role = "operator"
    else:
        role = "customer"

    hashed_password = pwd_context.hash(user.password)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO users (name, email, hashed_password, role, department)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (user.name, user.email, hashed_password, role, user.department)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"{role} registered successfully"}



# JWT config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Login request model (JSON)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(user: UserLogin):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # find user
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # create token
    token = create_access_token({
        "user_id": db_user["user_id"],
        "role": db_user["role"]
    })

    cursor.close()
    conn.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Load models
department_model = joblib.load("models/department_model.joblib")
priority_model = joblib.load("models/priority_model.joblib")

def predict_department_and_priority(text: str):
    # Models usually expect a list of inputs
    input_data = [text]

    # Department prediction
    dept_pred = department_model.predict(input_data)[0]
    dept_conf = max(department_model.predict_proba(input_data)[0])

    # Priority prediction
    prio_pred = priority_model.predict(input_data)[0]
    prio_conf = max(priority_model.predict_proba(input_data)[0])

    return {
        "department": dept_pred,
        "priority": prio_pred,
        "department_confidence": float(dept_conf),
        "priority_confidence": float(prio_conf)
    }

security = HTTPBearer()

def get_user_by_id(user_id):
    conn = get_db_connection()   # your existing function
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#get complaints
@app.get("/my-complaints")
def get_my_complaints(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT complaint_text, predicted_department, predicted_priority,
               department_confidence_score, priority_confidence_score, created_at
        FROM complaints
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (current_user["user_id"],))

    complaints = cursor.fetchall()

    cursor.close()
    conn.close()

    return complaints
    

class ComplaintCreate(BaseModel):
    complaint_text: str

@app.post("/submit-complaint")
def submit_complaint(
    complaint: ComplaintCreate,
    current_user = Depends(get_current_user)
):
    try:
        # 🔹 Run ML prediction
        prediction = predict_department_and_priority(complaint.complaint_text)

        department = prediction["department"]
        priority = prediction["priority"]
        dept_conf = prediction["department_confidence"]
        prio_conf = prediction["priority_confidence"]

        # 🔹 Apply thresholds
        if dept_conf < 0.5:
            department = None

        if prio_conf < 0.5:
            priority = None

        needs_review = (department == None) or (priority == None)
        # 🔹 Open DB connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 Insert into complaints table
        cursor.execute("""
            INSERT INTO complaints (
                user_id,
                complaint_text,
                predicted_department,
                predicted_priority,
                department_confidence_score,
                priority_confidence_score
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            current_user["user_id"],
            complaint.complaint_text,
            department,
            priority,
            dept_conf,
            prio_conf
        ))

        conn.commit()

        cursor.close()
        conn.close()

        # 🔹 Return response (matches frontend exactly)
        return {
            "department": department,
            "priority": priority,
            "needs_review": needs_review
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/operator-complaints")
def get_operator_complaints(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if current_user["role"] != "operator":
        raise HTTPException(status_code=403, detail="Not authorized")

    cursor.execute("""
        SELECT 
            c.complaint_text,
            c.predicted_department,
            c.predicted_priority,
            c.department_confidence_score,
            c.priority_confidence_score,
            c.created_at,
            u.name AS customer_name,
            u.user_id
        FROM complaints c
        JOIN users u ON c.user_id = u.user_id  
        WHERE c.predicted_department = %s
          AND c.predicted_priority IS NOT NULL
        ORDER BY c.created_at DESC
    """, (current_user["department"],))

    complaints = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "department": current_user["department"],   
        "complaints": complaints
    }

@app.get("/reviewer-complaints")
def get_reviewer_complaints(current_user = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if current_user["role"] != "reviewer":
        raise HTTPException(status_code=403, detail="Not authorized")

    cursor.execute("""
        SELECT 
            c.complaint_id,
            c.complaint_text,
            c.predicted_department,
            c.predicted_priority,
            c.department_confidence_score,
            c.priority_confidence_score,
            c.created_at,
            u.name AS customer_name,
            u.user_id AS user_id
        FROM complaints c
        JOIN users u ON c.user_id = u.user_id
        WHERE 
            c.predicted_department IS NULL
            OR c.predicted_priority IS NULL
        ORDER BY c.created_at DESC
    """)

    complaints = cursor.fetchall()

    cursor.close()
    conn.close()

    return complaints