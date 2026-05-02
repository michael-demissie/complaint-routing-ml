import os
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import S3_BUCKET_NAME, DEPT_MODEL_S3_PREFIX, DEPT_MODEL_LOCAL_DIR, ALLOWED_ORIGINS
from app.ml.predictor import load_models
from app.routes import auth, complaints, pages
from app.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="FinResolve Complaint Routing API",
    description="AI-powered complaint routing system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_model_from_s3():
    logger.info("Downloading department model from S3 bucket: %s", S3_BUCKET_NAME)
    try:
        s3 = boto3.client("s3")
        os.makedirs(DEPT_MODEL_LOCAL_DIR, exist_ok=True)
        objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=DEPT_MODEL_S3_PREFIX)
        for obj in objects.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):
                continue
            local_path = os.path.join(DEPT_MODEL_LOCAL_DIR, key.replace(DEPT_MODEL_S3_PREFIX + "/", ""))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(S3_BUCKET_NAME, key, local_path)
        logger.info("Department model downloaded successfully to %s", DEPT_MODEL_LOCAL_DIR)
    except Exception as e:
        logger.error("Failed to download model from S3: %s", str(e))
        raise

@app.on_event("startup")
def startup():
    logger.info("Starting FinResolve Complaint Routing API")
    download_model_from_s3()
    load_models()
    logger.info("API startup complete — ready to serve requests")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(complaints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
