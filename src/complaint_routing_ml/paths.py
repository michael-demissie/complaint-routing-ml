from pathlib import Path

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

ROOT = project_root()


DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

NOTEBOOKS_DIR = ROOT / "notebooks"
DOCS_DIR = ROOT / "docs"

def ensure_project_dirs() -> None:
    for p in [RAW_DIR, INTERIM_DIR, PROCESSED_DIR, NOTEBOOKS_DIR, DOCS_DIR]:
        p.mkdir(parents=True, exist_ok=True)


