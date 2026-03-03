from pathlib import path

def project_root() -> path:
    return path(__file__).resolve().parents[2]

ROOT = project_root()


DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = ROOT / "notebooks"

def ensure_data_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


