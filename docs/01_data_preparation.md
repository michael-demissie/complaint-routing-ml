# Data Preparation Summary

This document summarizes the preprocessing steps applied to the CFPB consumer complaints dataset before model training.

## 1. Convert CSV to Parquet
The raw CSV dataset was converted to **Parquet format** with Snappy compression to improve storage efficiency and loading speed.

## 2. Load and Inspect Data
The dataset was loaded from Parquet and basic checks were performed:
- Dataset size: **1,404,900 rows**
- Verified that complaint narratives were not missing.
- Explored category distributions (`Product`, `Sub-product`, `Issue`, `Sub-issue`).

## 3. Department Mapping
CFPB product categories were mapped to a smaller set of operational **departments** such as:
- Bank accounts
- Card services
- Credit reporting
- Debt collection
- Mortgage
- Consumer loans
- Payday / personal loans
- Student loan
- Money transfer services

A new column `Department` was created from the `Product` column.

## 4. Priority Assignment
A rule-based function assigned complaint urgency levels:
- **Immediate** – severe cases (e.g., hacked account, phishing).
- **Same-day** – urgent financial issues (e.g., unauthorized charge).
- **Regular** – all other complaints.

This label was stored in the `Priority` column.

## 5. Narrative Cleaning
Several cleaning steps were applied to the complaint text:

- Calculated word counts (`n_words`)
- Truncated narratives longer than **1000 words**
- Removed narratives shorter than **5 words**

A cleaned text column `clean_narrative` was created.

## 6. Remove Duplicates
Duplicate complaints were removed using:

- `clean_narrative`
- `Department`
- `Priority`

This reduced the dataset from **1.4M to less than 1M complaints**.

## 7. Create Modeling Dataset
The dataset was reduced to the columns required for modeling:

- `Complaint ID`
- `clean_narrative`
- `Department`
- `Priority`

## 8. Train/Test Split
The dataset was split into:

- **80% training**
- **20% testing**

Stratification was applied on the **Department** column to preserve class distribution.

## 9. Save Processed Data
Datasets were saved in Parquet format:

- `data/interim/cfpb_cleaned.parquet`
- `data/processed/train_complaints.parquet`
- `data/processed/test_complaints.parquet`