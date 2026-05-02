import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.config import (
    DEPT_ID2LABEL, PRIORITY_ID2LABEL,
    DEPT_MODEL_LOCAL_DIR, PRIORITY_MODEL_DIR
)

dept_tokenizer = None
dept_model = None
priority_tokenizer = None
priority_model = None

def load_models():
    global dept_tokenizer, dept_model, priority_tokenizer, priority_model
    dept_tokenizer = AutoTokenizer.from_pretrained(DEPT_MODEL_LOCAL_DIR)
    dept_model = AutoModelForSequenceClassification.from_pretrained(DEPT_MODEL_LOCAL_DIR)
    dept_model.eval()
    priority_tokenizer = AutoTokenizer.from_pretrained(PRIORITY_MODEL_DIR)
    priority_model = AutoModelForSequenceClassification.from_pretrained(PRIORITY_MODEL_DIR)
    priority_model.eval()

def predict_department_and_priority(text: str) -> dict:
    dept_inputs = dept_tokenizer(
        text, return_tensors="pt", truncation=True, padding=True
    )
    with torch.no_grad():
        outputs = dept_model(**dept_inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        confidence, pred_class = torch.max(probs, dim=1)
        dept_pred = DEPT_ID2LABEL[pred_class.item()]
        dept_conf = float(confidence.item())

    prio_inputs = priority_tokenizer(
        text, return_tensors="pt", truncation=True, padding=True
    )
    with torch.no_grad():
        prio_outputs = priority_model(**prio_inputs)
        prio_probs = torch.softmax(prio_outputs.logits, dim=1)
        prio_confidence, prio_class = torch.max(prio_probs, dim=1)
        prio_pred = PRIORITY_ID2LABEL[prio_class.item()]
        prio_conf = float(prio_confidence.item())

    return {
        "department": dept_pred,
        "priority": prio_pred,
        "department_confidence": dept_conf,
        "priority_confidence": prio_conf
    }
