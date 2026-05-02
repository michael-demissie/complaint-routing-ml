from fastapi import APIRouter, HTTPException, Depends
from app.schemas.complaints import ComplaintCreate, ComplaintResponse
from app.database import get_db_connection
from app.dependencies import get_current_user
from app.ml.predictor import predict_department_and_priority
from app.config import CONFIDENCE_THRESHOLD
from app.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

def row_to_dict(cursor, row):
    return {desc[0]: row[i] for i, desc in enumerate(cursor.description)}

def rows_to_dicts(cursor, rows):
    return [row_to_dict(cursor, r) for r in rows]

@router.get("/my-complaints")
def get_my_complaints(current_user=Depends(get_current_user)):
    logger.info("Fetching complaints | user_id=%s", current_user["user_id"])
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT complaint_text, predicted_department, predicted_priority,
                   department_confidence_score, priority_confidence_score, created_at
            FROM complaints
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (current_user["user_id"],))
        return rows_to_dicts(cursor, cursor.fetchall())
    finally:
        cursor.close()
        conn.close()

@router.post("/submit-complaint", response_model=ComplaintResponse)
def submit_complaint(complaint: ComplaintCreate, current_user=Depends(get_current_user)):
    logger.info("Complaint submitted | user_id=%s", current_user["user_id"])
    prediction = predict_department_and_priority(complaint.complaint_text)
    dept = prediction["department"] if prediction["department_confidence"] >= CONFIDENCE_THRESHOLD else None
    prio = prediction["priority"] if prediction["priority_confidence"] >= CONFIDENCE_THRESHOLD else None
    if dept is None:
        logger.warning("Low department confidence | score=%.2f | user_id=%s", prediction["department_confidence"], current_user["user_id"])
    if prio is None:
        logger.warning("Low priority confidence | score=%.2f | user_id=%s", prediction["priority_confidence"], current_user["user_id"])
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO complaints (
                user_id, complaint_text, predicted_department,
                predicted_priority, department_confidence_score, priority_confidence_score
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_user["user_id"], complaint.complaint_text, dept, prio,
              prediction["department_confidence"], prediction["priority_confidence"]))
        conn.commit()
        logger.info("Complaint saved | user_id=%s | dept=%s | priority=%s", current_user["user_id"], dept, prio)
    finally:
        cursor.close()
        conn.close()
    return {"department": dept, "priority": prio}

@router.get("/operator-complaints")
def get_operator_complaints(current_user=Depends(get_current_user)):
    if current_user["role"] != "operator":
        logger.warning("Unauthorized operator access | user_id=%s | role=%s", current_user["user_id"], current_user["role"])
        raise HTTPException(status_code=403, detail="Not authorized")
    logger.info("Operator fetching complaints | dept=%s", current_user["department"])
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.complaint_text, c.predicted_department, c.predicted_priority,
                   c.department_confidence_score, c.priority_confidence_score,
                   c.created_at, u.name AS customer_name, u.user_id
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.predicted_department = %s
              AND c.predicted_priority IS NOT NULL
            ORDER BY c.created_at DESC
        """, (current_user["department"],))
        return {"department": current_user["department"], "complaints": rows_to_dicts(cursor, cursor.fetchall())}
    finally:
        cursor.close()
        conn.close()

@router.get("/reviewer-complaints")
def get_reviewer_complaints(current_user=Depends(get_current_user)):
    if current_user["role"] != "reviewer":
        logger.warning("Unauthorized reviewer access | user_id=%s | role=%s", current_user["user_id"], current_user["role"])
        raise HTTPException(status_code=403, detail="Not authorized")
    logger.info("Reviewer fetching low-confidence complaints")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.complaint_id, c.complaint_text, c.predicted_department,
                   c.predicted_priority, c.department_confidence_score,
                   c.priority_confidence_score, c.created_at,
                   u.name AS customer_name, u.user_id
            FROM complaints c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.predicted_department IS NULL OR c.predicted_priority IS NULL
            ORDER BY c.created_at DESC
        """)
        return rows_to_dicts(cursor, cursor.fetchall())
    finally:
        cursor.close()
        conn.close()
