## Baseline Model Training and Evaluation Summary

- Loaded processed train and test datasets from Parquet files  
  - Train shape: (798,916, 4)  
  - Test shape: (199,730, 4)

- Defined features and targets  
  - Feature: `clean_narrative`  
  - Targets: `Department` and `Priority`

---

## Baseline Models (Naive Bayes)

### Department Classification
- Pipeline: TF-IDF + MultinomialNB  
- Accuracy: **~0.82**  
- Strong performance on:
  - Credit reporting (F1 ~0.90)
  - Mortgage (F1 ~0.83)
- Weak performance on:
  - Payday / personal loans (F1 very low)

### Priority Classification
- Pipeline: TF-IDF + MultinomialNB  
- Accuracy: **~0.92**  
- Strong performance on:
  - Regular (F1 ~0.96)
- Weak performance on:
  - Immediate (F1 ~0.50)

- Confusion matrices plotted for both tasks

---

## Improved Models (Logistic Regression)

### Department Classification
- Pipeline: TF-IDF + Logistic Regression  
- Accuracy: **~0.87**  
- Improved F1 across most classes  
- Better balance compared to Naive Bayes

### Priority Classification
- Pipeline: TF-IDF + Logistic Regression  
- Accuracy: **~0.94–0.95**  
- Strong performance on:
  - Regular (F1 ~0.97)
  - Same-day (F1 ~0.82)
- Immediate class still relatively weaker

---

## Class Imbalance Experiment

- Logistic Regression with `class_weight="balanced"` tested
- Result:
  - Slight drop in overall accuracy (~0.83)
  - Mixed impact on minority classes
  - Not clearly better than default LR

---

## Key Takeaways

- Logistic Regression outperforms Naive Bayes for both tasks  
- Priority model performs better than department model overall  
- Class imbalance significantly affects minority classes (especially Immediate and Payday loans)  
- Weighted metrics are high, but macro scores reveal imbalance issues  