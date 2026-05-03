"""
Priority model training script.
Uses TF-IDF + LightGBM for fast, reliable priority classification.
Run from project root: python -m app.ml.train_priority
"""
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import re
import os

# ── config ────────────────────────────────────────────────────────────────────

TRAIN_PATH = "data/processed/train_complaints.parquet"
TEST_PATH  = "data/processed/test_complaints.parquet"
MODEL_DIR  = "models/priority-lgbm"
os.makedirs(MODEL_DIR, exist_ok=True)

# ── preprocessing ─────────────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # remove CFPB masks
    text = re.sub(r'\b[x]{2}/[x]{2}/[x]{4}\b', ' ', text)
    text = re.sub(r'\b[x]{2,}\d*\b', ' ', text)
    # remove dollar amounts pattern but keep the word "dollars"
    text = re.sub(r'\{\$[\d,]+\.\d+\}', ' money_amount ', text)
    # normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ── load data ─────────────────────────────────────────────────────────────────

print("Loading data...")
train_df = pd.read_parquet(TRAIN_PATH)
test_df  = pd.read_parquet(TEST_PATH)

print(f"Train size: {len(train_df):,}")
print(f"Test size:  {len(test_df):,}")
print()
print("Priority distribution (train):")
print(train_df["Priority"].value_counts())

# ── feature engineering ───────────────────────────────────────────────────────

print("\nPreprocessing text...")
X_train = train_df["Consumer complaint narrative"].apply(preprocess)
X_test  = test_df["Consumer complaint narrative"].apply(preprocess)

# Encode labels
le = LabelEncoder()
y_train = le.fit_transform(train_df["Priority"])
y_test  = le.transform(test_df["Priority"])

print("Label encoding:", dict(zip(le.classes_, le.transform(le.classes_))))

# ── model pipeline ────────────────────────────────────────────────────────────

print("\nBuilding pipeline...")
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=50000,      # top 50k most important words
        ngram_range=(1, 2),      # unigrams and bigrams
        min_df=3,                # ignore very rare words
        max_df=0.95,             # ignore very common words
        sublinear_tf=True,       # apply log normalization
    )),
    ("clf", LGBMClassifier(
        n_estimators=500,        # number of trees
        learning_rate=0.05,      # step size
        num_leaves=63,           # tree complexity
        class_weight="balanced", # handle any remaining imbalance
        random_state=42,
        n_jobs=-1,               # use all CPU cores
        verbose=-1,              # suppress training output
    ))
])

# ── train ─────────────────────────────────────────────────────────────────────

print("Training model...")
pipeline.fit(X_train, y_train)
print("Training complete.")

# ── evaluate ──────────────────────────────────────────────────────────────────

print("\nEvaluating on test set...")
y_pred = pipeline.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)
print(cm_df)

# ── save ──────────────────────────────────────────────────────────────────────

print("\nSaving model...")
joblib.dump(pipeline, f"{MODEL_DIR}/pipeline.joblib")
joblib.dump(le, f"{MODEL_DIR}/label_encoder.joblib")
print(f"Model saved to {MODEL_DIR}/")

print("\nDone.")
