import re
import warnings
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.config import DEPT_ID2LABEL, DEPT_MODEL_LOCAL_DIR
from app.logger import get_logger

logger = get_logger(__name__)

PRIORITY_MODEL_DIR = "models/priority-lgbm"

# Load LightGBM first to avoid OpenMP conflict with PyTorch on some systems
priority_pipeline = None
priority_le       = None
dept_tokenizer    = None
dept_model        = None

def load_models():
    global priority_pipeline, priority_le, dept_tokenizer, dept_model

    # LightGBM must be loaded before PyTorch
    logger.info("Loading priority model from %s", PRIORITY_MODEL_DIR)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        priority_pipeline = joblib.load(f"{PRIORITY_MODEL_DIR}/pipeline.joblib")
        priority_le       = joblib.load(f"{PRIORITY_MODEL_DIR}/label_encoder.joblib")
    logger.info("Priority model loaded successfully")

    logger.info("Loading department model from %s", DEPT_MODEL_LOCAL_DIR)
    dept_tokenizer = AutoTokenizer.from_pretrained(DEPT_MODEL_LOCAL_DIR)
    dept_model     = AutoModelForSequenceClassification.from_pretrained(DEPT_MODEL_LOCAL_DIR)
    dept_model.eval()
    logger.info("Department model loaded successfully")

def _preprocess(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\b[x]{2}/[x]{2}/[x]{4}\b', ' ', text)
    text = re.sub(r'\b[x]{2,}\d*\b', ' ', text)
    text = re.sub(r'\{\$[\d,]+\.\d+\}', ' money_amount ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict_department_and_priority(text: str) -> dict:
    try:
        # ── department prediction (BERT) ──────────────────────────────────────
        dept_inputs = dept_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            outputs   = dept_model(**dept_inputs)
            probs     = torch.softmax(outputs.logits, dim=1)
            conf, idx = torch.max(probs, dim=1)
            dept_pred = DEPT_ID2LABEL[idx.item()]
            dept_conf = float(conf.item())

        # ── priority prediction (LightGBM) ────────────────────────────────────
        cleaned = _preprocess(text)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            proba = priority_pipeline.predict_proba([cleaned])[0]
        prio_conf = float(proba.max())
        prio_pred = priority_le.inverse_transform([proba.argmax()])[0]

        logger.info(
            "Prediction | dept=%s (%.2f) | priority=%s (%.2f)",
            dept_pred, dept_conf, prio_pred, prio_conf
        )

        return {
            "department":            dept_pred,
            "priority":              prio_pred,
            "department_confidence": dept_conf,
            "priority_confidence":   prio_conf,
        }

    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        raise
