# Data Splitting and ID Strategy

## Stable Complaint ID

- A stable complaint ID is created for each complaint.
- This allows us to connect the departmental model results with the priority classification model later.

---

## Train and Test Split

- The dataset is split into training and test sets before designing any models.
- The split keeps the same proportion of each department in both sets (stratified split).

---

## Saving the Split

- The train and test sets are saved.
- These saved splits are used for all departmental models to ensure consistency.

---

## Priority Classification Model

- The priority classification model will use the same train and test split.
- New priority classes will be created later through feature engineering.