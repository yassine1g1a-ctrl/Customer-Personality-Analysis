"""
One-time setup script: prepares the notebooks for Prefect + papermill execution.
- Tags parameter cells in NB01 and NB02
- Inserts a parameters cell in NB03, NB04, NB05
- Fixes hardcoded CSV paths to use DATA_IN variable
Run once before deploying: python setup_prefect_notebooks.py
"""
import json
import copy
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def load_nb(name: str) -> dict:
    path = os.path.join(BASE, name)
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f), path


def save_nb(nb: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"  Saved {os.path.basename(path)}")


def make_code_cell(source_lines: list[str], tags: list[str] | None = None) -> dict:
    cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": tags or []},
        "outputs": [],
        "source": source_lines,
    }
    return cell


# ─────────────────────────────────────────────────────────────────────────────
# NB01 – Feature Engineering
# Tag cell 1 (imports + DATA_IN/DATA_OUT) and fix default paths
# ─────────────────────────────────────────────────────────────────────────────
print("\n[NB01] Feature Engineering …")
nb, path = load_nb("01_Feature_Engineering.ipynb")

cell1 = nb["cells"][1]
# Update default paths to include data/ prefix
src = "".join(cell1["source"])
src = src.replace(
    'DATA_IN  = "cleaned_marketing_campaign.csv"',
    'DATA_IN  = "data/cleaned_marketing_campaign.csv"',
)
src = src.replace(
    'DATA_IN = "cleaned_marketing_campaign.csv"',
    'DATA_IN = "data/cleaned_marketing_campaign.csv"',
)
src = src.replace(
    'DATA_OUT = "customers_featured.csv"',
    'DATA_OUT = "data/customers_featured.csv"',
)
cell1["source"] = src.splitlines(keepends=True)
cell1["metadata"]["tags"] = ["parameters"]
print("  Tagged cell 1 as 'parameters', fixed default paths.")
save_nb(nb, path)


# ─────────────────────────────────────────────────────────────────────────────
# NB02 – EDA
# Tag cell 1 and fix DATA_IN default
# ─────────────────────────────────────────────────────────────────────────────
print("\n[NB02] EDA …")
nb, path = load_nb("02_Exploratory_Data_Analysis.ipynb")

cell1 = nb["cells"][1]
src = "".join(cell1["source"])
src = src.replace(
    'DATA_IN = "customers_featured.csv"',
    'DATA_IN = "data/customers_featured.csv"',
)
cell1["source"] = src.splitlines(keepends=True)
cell1["metadata"]["tags"] = ["parameters"]
print("  Tagged cell 1 as 'parameters', fixed default DATA_IN path.")
save_nb(nb, path)


# ─────────────────────────────────────────────────────────────────────────────
# NB03 – Clustering
# Insert a tagged parameters cell before the imports cell,
# then replace hardcoded read_csv with DATA_IN
# ─────────────────────────────────────────────────────────────────────────────
print("\n[NB03] Clustering …")
nb, path = load_nb("03_Clustering_Models.ipynb")

# Insert parameters cell at position 0 (top of notebook)
params_src = [
    "# --- Parameters (overridden by Prefect / papermill)\n",
    'DATA_IN     = "data/customers_featured.csv"\n',
    "RANDOM_SEED = 42\n",
    "ENCODING_DIM = 10\n",
    "EPOCHS      = 50\n",
    "BATCH_SIZE  = 32\n",
    "N_CLUSTERS  = 5\n",
]
params_cell = make_code_cell(params_src, tags=["parameters"])
nb["cells"].insert(0, params_cell)

# Replace hardcoded read_csv (now shifted: data-load cell was 3, now 4)
fixed = 0
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        src = "".join(cell["source"])
        new_src = src.replace('pd.read_csv("customers_featured.csv")', "pd.read_csv(DATA_IN)")
        if new_src != src:
            cell["source"] = new_src.splitlines(keepends=True)
            fixed += 1

print(f"  Inserted parameters cell at position 0.")
print(f"  Replaced hardcoded read_csv in {fixed} cell(s).")
save_nb(nb, path)


# ─────────────────────────────────────────────────────────────────────────────
# NB04 – Classification
# Insert parameters cell at position 0, replace all 8 hardcoded occurrences
# ─────────────────────────────────────────────────────────────────────────────
print("\n[NB04] Classification …")
nb, path = load_nb("04_Classification_Models.ipynb")

params_src = [
    "# --- Parameters (overridden by Prefect / papermill)\n",
    'DATA_IN      = "data/customers_featured.csv"\n',
    "TEST_SIZE    = 0.2\n",
    "RANDOM_STATE = 42\n",
    "LR_MAX_ITER  = 1000\n",
    "RF_N_ESTIMATORS = 200\n",
    "DL_EPOCHS    = 70\n",
    "DL_RF_EPOCHS = 150\n",
    "BATCH_SIZE   = 32\n",
    "LEARNING_RATE = 0.001\n",
]
params_cell = make_code_cell(params_src, tags=["parameters"])
nb["cells"].insert(0, params_cell)

fixed = 0
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        src = "".join(cell["source"])
        new_src = src.replace('pd.read_csv("customers_featured.csv")', "pd.read_csv(DATA_IN)")
        if new_src != src:
            cell["source"] = new_src.splitlines(keepends=True)
            fixed += 1

print(f"  Inserted parameters cell at position 0.")
print(f"  Replaced hardcoded read_csv in {fixed} cell(s).")
save_nb(nb, path)


# ─────────────────────────────────────────────────────────────────────────────
# NB05 – Model Evaluation
# Insert parameters cell at position 0, replace 2 hardcoded occurrences
# ─────────────────────────────────────────────────────────────────────────────
print("\n[NB05] Model Evaluation …")
nb, path = load_nb("05_Model_Evaluation.ipynb")

params_src = [
    "# --- Parameters (overridden by Prefect / papermill)\n",
    'DATA_IN      = "data/customers_featured.csv"\n',
    "TEST_SIZE    = 0.2\n",
    "RANDOM_STATE = 42\n",
    "THRESHOLD    = 0.5\n",
    "TOP_N_FEATURES = 15\n",
]
params_cell = make_code_cell(params_src, tags=["parameters"])
nb["cells"].insert(0, params_cell)

fixed = 0
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        src = "".join(cell["source"])
        new_src = src.replace('pd.read_csv("customers_featured.csv")', "pd.read_csv(DATA_IN)")
        if new_src != src:
            cell["source"] = new_src.splitlines(keepends=True)
            fixed += 1

print(f"  Inserted parameters cell at position 0.")
print(f"  Replaced hardcoded read_csv in {fixed} cell(s).")
save_nb(nb, path)

print("\n✓ All notebooks prepared for Prefect + papermill.")
