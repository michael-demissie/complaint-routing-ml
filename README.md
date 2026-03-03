# Complaint Routing ML

Machine learning pipeline for classifying CFPB consumer complaints into departments and priority levels.

---

## 1. Project Structure
complaint-routing-ml/
│
├── data/
│ ├── raw/ # Original downloaded data (not committed to git)
│ ├── interim/ # Cleaned intermediate datasets
│ └── processed/ # Model-ready datasets
│
├── notebooks/ # Step-by-step ML workflow
├── src/ # Reusable project modules
├── docs/ # Documentation
│
├── pyproject.toml
└── README.md


---

## 2. Quick Start (Local: Mac / Windows)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/mikaelAbyssinia/complaint-routing-ml.git
cd complaint-routing-ml
```

### Step 2 — Create Virtual Environment
```bash
python -m venv .venv   
```

#### Activate it
Mac / Linux
```
source .venv/bin/activate
```
Windows
```
.venv\Scripts\activate
```
### Step 3 — Install Dependencies
```
pip install -U pip
pip install -e .
```

### Step 4 — Launch Jupyter
```
jupyter lab
```
Open notebooks inside the notebooks/ folder and run them in numerical order.

## 3. Quick Start (Google Colab)
Run the following cells:
```
!git clone https://github.com/mikaelAbyssinia/complaint-routing-ml.git
%cd complaint-routing-ml
!pip install -e .
```
Then open the desired notebook from the notebooks/ directory.

## 4. Download Original Dataset

Download the CFPB Consumer Complaints dataset:

[Download Original CFPB Complaints CSV (2011-12-01 to 2026-02-26, Narratives Only)](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?date_received_max=2026-02-26&date_received_min=2011-12-01&field=all&format=csv&has_narrative=true&no_aggs=true&size=3731229)

After downloading, place the CSV file inside:
``` data/raw/
```

Do not rename the file unless instructed in the notebook.

## 5. Notebook Execution Order
Run notebooks in numerical order:
```
01_data_cleaning.ipynb
02_eda.ipynb
03_department_baseline_nb.ipynb
04_department_tfidf_experiment.ipynb
05_priority_label_engineering.ipynb
06_priority_model.ipynb
```

## 6. Notes
-- The data/ folder is excluded from git.
-- Use pip install -e . to ensure imports work correctly.
-- File paths are handled automatically through the paths.py module.
-- Designed to work on Mac, Windows, and Google Colab.

## 7. License
For academic and educational purposes.