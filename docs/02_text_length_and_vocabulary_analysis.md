# Text Length and Vocabulary Observations

## General Findings

- Extremely short complaints are negligible (about 0.13% of the data).
- There are some outliers with very long word counts.
- There is no extreme imbalance in text length across departments.
- No department is systematically too short. Even the smallest class has a reasonable average text length.

---

## Interpretation

Most departments appear linguistically separable based on vocabulary patterns.  
This suggests that a text classification model should be able to learn meaningful differences between categories.

The only potentially weak class is **Financial Services Support**, due to its small size and overlapping terminology, which may lead to lower performance for that category.