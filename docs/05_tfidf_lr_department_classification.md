### Logistic Regression with TF-IDF

- We remove mask tokens such as **`xxxx`** and **`xx`** from the data.  
- Then we use a pipeline that applies **TF-IDF vectorization**. This removes stop words and filters out very rare and very frequent tokens, along with other basic cleaning steps.  
- The resulting vectorized matrix is then passed to a **Logistic Regression (LR)** model.

---

### 1. LR with `class_weight="balanced"`

This setting penalizes mistakes on **small classes** more.

Balanced training tells the model **not to optimize only for the largest class**.  
Because of this, the model sacrifices some performance on large classes in order to help smaller classes.

**Macro F1 = 0.74**

However, routing systems mainly care about **overall correct routing**, and large departments dominate real traffic.  
Balanced models are usually used when **minority classes are critical**.

Therefore, we trained the model again **without the balanced weights**.

---

### 2. LR without `class_weight`

#### Major improvements (LR vs Naive Bayes baseline)

**Credit Reporting**

- NB F1: **0.91**  
- LR F1: **0.95**

Already strong, but LR improved recall significantly.

---

**Bank Accounts**

- NB F1: **0.76**  
- LR F1: **0.82**

Better balance between precision and recall.

---

**Debt Collection**

- NB F1: **0.68**  
- LR F1: **0.77**

Big improvement.

---

**Money Transfers**

- NB F1: **0.75**  
- LR F1: **0.83**

Large improvement.

---

**Credit or Prepaid Cards**

- NB F1: **0.65**  
- LR F1: **0.78**

Very large improvement.

---

### Still weak classes

**Consumer Loans**

- NB F1: **0.42**  
- LR F1: **0.52**

Still difficult. This likely comes from **overlap with Mortgage and Vehicle loan complaints**.

---

**Vehicle loan or lease**

- NB F1: **0.55**  
- LR F1: **0.63**

Improved but still weak.

---

### Next step → TF-IDF + Linear SVM

SVM works extremely well with **high-dimensional sparse text vectors**.

Logistic Regression tries to **fit probabilities**.  
SVM instead tries to **separate classes with the largest possible margin**.

**Expectation:** SVM may improve **macro-F1 by about 2–4%**.