import os
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import S3_BUCKET_NAME, DEPT_MODEL_S3_PREFIX, DEPT_MODEL_LOCAL_DIR, ALLOWED_ORIGINS, PRIORITY_MODEL_DIR
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

def model_exists(local_dir: str) -> bool:
    return os.path.exists(os.path.join(local_dir, "config.json")) and \
           os.path.exists(os.path.join(local_dir, "model.safetensors"))

def download_folder_from_s3(bucket, prefix, local_dir):
    s3 = boto3.client("s3")
    os.makedirs(local_dir, exist_ok=True)
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in objects.get("Contents", []):
        key = obj["Key"]
        if key.endswith("/"):
            continue
        local_path = os.path.join(local_dir, key.replace(prefix + "/", ""))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3.download_file(bucket, key, local_path)

@app.on_event("startup")
def startup():
    logger.info("Starting FinResolve Complaint Routing API")

    if model_exists(DEPT_MODEL_LOCAL_DIR):
        logger.info("Department model already cached, skipping S3 download")
    else:
        logger.info("Downloading department model from S3...")
        download_folder_from_s3(S3_BUCKET_NAME, DEPT_MODEL_S3_PREFIX, DEPT_MODEL_LOCAL_DIR)
        logger.info("Department model downloaded successfully")

    if model_exists(PRIORITY_MODEL_DIR):
        logger.info("Priority model already cached, skipping S3 download")
    else:
        logger.info("Downloading priority model from S3...")
        download_folder_from_s3(S3_BUCKET_NAME, "priority-model-bert", PRIORITY_MODEL_DIR)
        logger.info("Priority model downloaded successfully")

    load_models()
    logger.info("API startup complete — ready to serve requests")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(complaints.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
