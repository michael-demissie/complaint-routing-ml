# Baseline Model: Multinomial Naive Bayes

## Model Overview

This is the first simple text classification model in the project.

- **CountVectorizer** converts complaint text into numbers by counting how many times each word appears (bag-of-words).
- **Multinomial Naive Bayes** uses those word counts to estimate the probability of each department and predicts the most likely class.
- The **Pipeline** connects these steps so text is automatically transformed and classified during training and prediction.

---

## Overall Performance

- **Accuracy:** 0.83  
- **Weighted F1:** 0.84  
- **Macro F1:** 0.63  

### Interpretation

- Overall performance looks strong.
- But Macro F1 is much lower than Weighted F1.
- That gap confirms a class imbalance problem.

The model almost never predicts the **Financial Services Support** class.

Bag-of-words works well for dominant departments but struggles with rare categories.  
Class imbalance heavily affects minority classes.

---

## Summary

The Multinomial Naive Bayes model reaches **83% accuracy**, with strong performance on dominant classes such as **Credit Reporting** and **Mortgage**.

However, **macro-F1 (0.63)** shows weak performance on minority classes, especially **Financial Services Support**.

---

# Financial Services Support Department Analysis

- **Support:** 367 (extremely small)
- **Recall:** 0.01
- **F1:** 0.01
- Almost never predicted

This strongly suggests:

1. The class is poorly defined  
2. It overlaps heavily with other categories  
3. It may be a catch-all or residual bucket  
4. The model cannot learn clear boundaries  

So, this is mainly a **label problem**.

The model distributes this class across almost all other departments.  
That indicates the class does **not** have a distinctive vocabulary pattern.

---

# Removing the Department

## Pros

- Cleaner label space  
- Improved macro F1  
- More realistic routing system  
- Simpler model  

## Cons

- Slight data reduction (~0.13%)

Given the dataset size, this reduction is negligible.

This shows that improving performance can come from improving the problem definition, not increasing model complexity.

---

# Evaluation After Removing "Financial Services Support"

## Before Removing

- Accuracy ≈ 0.83  
- Macro F1 ≈ 0.63  

## After Removing

- Accuracy = 0.83 (unchanged)  
- Macro F1 = 0.70 (big improvement)  

Removing that class did not harm separability of the remaining classes.

---

# What Remains Weak

## Consumer Loans

- Recall = 0.39  
- F1 = 0.42  

This is now the main modeling challenge.

---

# Next Step

**Logistic Regression + TF-IDF**