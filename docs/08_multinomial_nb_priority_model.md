# Priority Classification Model

This notebook trains a machine learning model to classify consumer complaints into three urgency levels:

- immediate  
- same_day  
- regular  

The objective is to simulate a simple complaint triage system that can estimate how urgent a complaint is based on the narrative text.

---

# Data

The model uses two processed datasets:

- `priority_train.parquet`
- `priority_test.parquet`

Each record contains:

- complaint_id  
- Consumer complaint narrative  
- priority (target label)

The dataset is split into features (`X_train`, `X_test`) and target labels (`y_train`, `y_test`).

---

# Text Cleaning

Complaint narratives sometimes contain masked tokens such as sequences of `x`.  
A regex cleaning step removes words containing these masked patterns because they do not carry useful semantic information for the model.

---

# Feature Engineering

Two stylistic features were extracted from the complaint narrative:

**Repeated exclamation marks**

Counts occurrences of repeated `!`. Multiple exclamation marks can indicate urgency.

**Capitalization ratio**

Measures the proportion of fully capitalized words relative to the total number of words in the complaint. High capitalization may signal emphasis or urgency.

---

# Text Representation

The complaint narratives were converted into numerical features using:

`CountVectorizer(stop_words="english")`

This creates a bag-of-words representation of the text while removing common English stop words.

---

# Feature Combination

The final feature set combines:

- bag-of-words text features
- stylistic features (`exclam_flag`, `caps_ratio`)

The two style features were multiplied by a small factor to increase their influence relative to the large number of word features.  
All features were combined using `scipy.sparse.hstack`.

---

# Model

A **Multinomial Naive Bayes** classifier was trained on the combined feature matrix.  
This model is commonly used for text classification because it works well with word count features.

---

# Evaluation

The model achieves an overall **accuracy of about 0.74**.

From the evaluation results:

- **Regular complaints are predicted best**, with the highest precision and recall.  
- **Immediate complaints are reasonably detected**, with recall around **0.70**, meaning the model captures many urgent complaints.  
- **Same_day complaints are harder to identify**, with lower recall, suggesting the language used in these complaints overlaps with the other two classes.

For this task, **recall for the urgent classes (especially "immediate") is the most important metric**, since missing an urgent complaint is more problematic than incorrectly flagging a regular one.

Overall, the model shows that basic text features combined with simple stylistic signals can provide a reasonable baseline for complaint priority classification.