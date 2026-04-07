"""
Customer Personality Analysis – Prefect Pipeline
=================================================
Executes the 5 notebooks in order using papermill.

Usage (local):
    python pipeline.py

Deploy to Prefect Cloud:
    uvx prefect-cloud login
    uvx prefect-cloud github setup
    uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
        --from <github-account>/<repo-name> \
        --name customer-analysis-pipeline

Run a deployed flow:
    uvx prefect-cloud run customer_personality_pipeline/customer-analysis-pipeline

Schedule (daily at midnight UTC):
    uvx prefect-cloud schedule customer_personality_pipeline/customer-analysis-pipeline "0 0 * * *"
"""

import os

import papermill as pm
from prefect import flow, task
from prefect.logging import get_run_logger

# ---------------------------------------------------------------------------
# Paths — relative to the repo root (where this file lives)
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
NB_DIR = REPO_ROOT  # notebooks are at the root


def _nb(name: str) -> str:
    """Absolute path to a notebook."""
    return os.path.join(NB_DIR, name)


def _out(name: str) -> str:
    """Output notebook goes next to the original with an _output suffix."""
    base, ext = os.path.splitext(name)
    return os.path.join(NB_DIR, f"{base}_output{ext}")


# ---------------------------------------------------------------------------
# Tasks — one per notebook
# ---------------------------------------------------------------------------

@task(name="01 – Feature Engineering", retries=1, retry_delay_seconds=30)
def run_feature_engineering(
    data_in: str = "data/cleaned_marketing_campaign.csv",
    data_out: str = "data/customers_featured.csv",
    random_seed: int = 42,
) -> str:
    logger = get_run_logger()
    logger.info("Starting Feature Engineering …")
    pm.execute_notebook(
        _nb("01_Feature_Engineering.ipynb"),
        _out("01_Feature_Engineering.ipynb"),
        parameters={
            "DATA_IN": data_in,
            "DATA_OUT": data_out,
            "RANDOM_SEED": random_seed,
        },
        cwd=REPO_ROOT,
        kernel_name="python3",
    )
    logger.info(f"Feature Engineering done → {data_out}")
    return data_out


@task(name="02 – Exploratory Data Analysis", retries=1, retry_delay_seconds=30)
def run_eda(
    data_in: str = "data/customers_featured.csv",
    fig_dir: str = "reports/figs",
    tab_dir: str = "reports/tables",
    random_seed: int = 42,
) -> None:
    logger = get_run_logger()
    logger.info("Starting EDA …")
    pm.execute_notebook(
        _nb("02_Exploratory_Data_Analysis.ipynb"),
        _out("02_Exploratory_Data_Analysis.ipynb"),
        parameters={
            "DATA_IN": data_in,
            "FIG_DIR": fig_dir,
            "TAB_DIR": tab_dir,
            "RANDOM_SEED": random_seed,
        },
        cwd=REPO_ROOT,
        kernel_name="python3",
    )
    logger.info("EDA done.")


@task(name="03 – Clustering Models", retries=1, retry_delay_seconds=60)
def run_clustering(
    data_in: str = "data/customers_featured.csv",
    random_seed: int = 42,
    encoding_dim: int = 10,
    epochs: int = 50,
    batch_size: int = 32,
    n_clusters: int = 5,
) -> None:
    logger = get_run_logger()
    logger.info("Starting Clustering …")
    pm.execute_notebook(
        _nb("03_Clustering_Models.ipynb"),
        _out("03_Clustering_Models.ipynb"),
        parameters={
            "DATA_IN": data_in,
            "RANDOM_SEED": random_seed,
            "ENCODING_DIM": encoding_dim,
            "EPOCHS": epochs,
            "BATCH_SIZE": batch_size,
            "N_CLUSTERS": n_clusters,
        },
        cwd=REPO_ROOT,
        kernel_name="python3",
    )
    logger.info("Clustering done.")


@task(name="04 – Classification Models", retries=1, retry_delay_seconds=60)
def run_classification(
    data_in: str = "data/customers_featured.csv",
    test_size: float = 0.2,
    random_state: int = 42,
    lr_max_iter: int = 1000,
    rf_n_estimators: int = 200,
    dl_epochs: int = 70,
    dl_rf_epochs: int = 150,
    batch_size: int = 32,
    learning_rate: float = 0.001,
) -> None:
    logger = get_run_logger()
    logger.info("Starting Classification Models …")
    pm.execute_notebook(
        _nb("04_Classification_Models.ipynb"),
        _out("04_Classification_Models.ipynb"),
        parameters={
            "DATA_IN": data_in,
            "TEST_SIZE": test_size,
            "RANDOM_STATE": random_state,
            "LR_MAX_ITER": lr_max_iter,
            "RF_N_ESTIMATORS": rf_n_estimators,
            "DL_EPOCHS": dl_epochs,
            "DL_RF_EPOCHS": dl_rf_epochs,
            "BATCH_SIZE": batch_size,
            "LEARNING_RATE": learning_rate,
        },
        cwd=REPO_ROOT,
        kernel_name="python3",
    )
    logger.info("Classification done.")


@task(name="05 – Model Evaluation", retries=1, retry_delay_seconds=30)
def run_evaluation(
    data_in: str = "data/customers_featured.csv",
    test_size: float = 0.2,
    random_state: int = 42,
    threshold: float = 0.5,
    top_n_features: int = 15,
) -> None:
    logger = get_run_logger()
    logger.info("Starting Model Evaluation …")
    pm.execute_notebook(
        _nb("05_Model_Evaluation.ipynb"),
        _out("05_Model_Evaluation.ipynb"),
        parameters={
            "DATA_IN": data_in,
            "TEST_SIZE": test_size,
            "RANDOM_STATE": random_state,
            "THRESHOLD": threshold,
            "TOP_N_FEATURES": top_n_features,
        },
        cwd=REPO_ROOT,
        kernel_name="python3",
    )
    logger.info("Model Evaluation done.")


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

@flow(
    name="customer_personality_pipeline",
    description="Full ML pipeline: Feature Engineering → EDA → Clustering → Classification → Evaluation",
)
def customer_personality_pipeline(
    # ── Data ──
    raw_data: str = "data/cleaned_marketing_campaign.csv",
    featured_data: str = "data/customers_featured.csv",
    # ── Global ──
    random_seed: int = 42,
    # ── NB03 Clustering ──
    encoding_dim: int = 10,
    clustering_epochs: int = 50,
    n_clusters: int = 5,
    # ── NB04 Classification ──
    test_size: float = 0.2,
    rf_n_estimators: int = 200,
    dl_epochs: int = 70,
    dl_rf_epochs: int = 150,
    learning_rate: float = 0.001,
    # ── NB05 Evaluation ──
    threshold: float = 0.5,
    top_n_features: int = 15,
) -> None:
    """
    Executes the 5 notebooks sequentially (1 → 2 → 3 → 4 → 5).

    Dependency graph:
        01_Feature_Engineering  →  customers_featured.csv
                                      ├─ 02_EDA             (reports)
                                      ├─ 03_Clustering      (personas)
                                      └─ 04_Classification  (models)  →  05_Evaluation
    Notebooks 02, 03, 04 are independent after 01; they run sequentially
    here to respect the user's requested order and avoid resource contention.
    """
    # Each task call blocks until completion → strict 1 → 2 → 3 → 4 → 5 order.
    # (Prefect runs tasks synchronously when called directly without .submit())

    # Step 1 — build enriched feature set (produces customers_featured.csv)
    run_feature_engineering(
        data_in=raw_data,
        data_out=featured_data,
        random_seed=random_seed,
    )

    # Step 2 — exploratory analysis (charts + tables)
    run_eda(
        data_in=featured_data,
        random_seed=random_seed,
    )

    # Step 3 — unsupervised clustering (deep autoencoder + DEC)
    run_clustering(
        data_in=featured_data,
        random_seed=random_seed,
        encoding_dim=encoding_dim,
        epochs=clustering_epochs,
        n_clusters=n_clusters,
    )

    # Step 4 — supervised classification (LR, RF, Deep LR, Deep RF)
    run_classification(
        data_in=featured_data,
        test_size=test_size,
        random_state=random_seed,
        rf_n_estimators=rf_n_estimators,
        dl_epochs=dl_epochs,
        dl_rf_epochs=dl_rf_epochs,
        learning_rate=learning_rate,
    )

    # Step 5 — evaluate all 4 trained models (depends on NB04 outputs)
    run_evaluation(
        data_in=featured_data,
        test_size=test_size,
        random_state=random_seed,
        threshold=threshold,
        top_n_features=top_n_features,
    )


# ---------------------------------------------------------------------------
# Local entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    customer_personality_pipeline()
