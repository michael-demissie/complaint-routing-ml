import os
from dotenv import load_dotenv

load_dotenv()

# Security
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# AWS / S3
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "bert-department-model")
DEPT_MODEL_S3_PREFIX = os.getenv("DEPT_MODEL_S3_PREFIX", "Department_model_Bert")
DEPT_MODEL_LOCAL_DIR = os.getenv("DEPT_MODEL_LOCAL_DIR", "/tmp/models/department-model-bert")

# Models
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PRIORITY_MODEL_DIR = os.path.join(BASE_DIR, "..", "models", "priority-model-bert")

# API
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))

# Department label mapping
DEPT_ID2LABEL = {
    0: "Bank accounts",
    1: "Card services",
    2: "Consumer loans",
    3: "Credit reporting",
    4: "Debt collection",
    5: "Money transfer services",
    6: "Mortgage",
    7: "Payday / personal loans",
    8: "Student loan"
}

# Priority label mapping
PRIORITY_ID2LABEL = {
    0: "critical",
    1: "high_priority",
    2: "standard"
}
