## Linear SVM (TF-IDF) Results

The TF-IDF + Linear SVM model achieved the following performance on the test set.

**Overall metrics**

- Accuracy: **0.91**
- Macro F1: **0.79**
- Weighted F1: **0.90**

The model performs extremely well on **Credit Reporting**, which dominates the dataset and appears to have very distinctive vocabulary in complaint narratives. Performance is also strong for **Mortgage**, **Student Loan**, and **Money Transfers and Digital Payments**. 

Lower performance is observed for **Consumer Loans** and **Vehicle Loan or Lease**, suggesting that these categories share vocabulary with other lending-related complaints, making them harder to separate using simple linear text features.

---

## Comparison with Logistic Regression

When compared with the TF-IDF + Logistic Regression model, the Linear SVM shows **slightly better overall performance**.

| Metric | Logistic Regression | Linear SVM |
|---|---|---|
| Accuracy | 0.901 | **0.91** |
| Macro F1 | 0.782 | **0.79** |
| Weighted F1 | 0.899 | **0.90** |

Linear SVM improves performance for several departments, particularly **Student Loan**, **Debt Collection**, and **Vehicle Loan or Lease**, indicating slightly better handling of minority classes. Logistic Regression performs similarly on most large classes, especially **Credit Reporting**, where both models achieve very high scores.

Overall, both models produce strong results for the complaint routing task, but **Linear SVM provides a small but consistent improvement in balanced performance across departments**.