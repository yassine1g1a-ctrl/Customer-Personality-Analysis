# Customer Personality Analysis

End-to-end data mining pipeline for **customer segmentation** and **marketing campaign response prediction**, following the CRISP-DM methodology.

Built as a group project for the course **D7043E – Advanced Data Mining** at Luleå University of Technology.

## Authors

| Name | Role |
|------|------|
| Bardia Baigy | Data Engineering, Feature Engineering |
| Dominic Addo | Classification Models |
| Abdalrahman Nasser | Deep Learning Models |
| Yassine Taharaste | EDA, Clustering, Evaluation |
| Deborah Aittokallio | Data Cleaning, Reporting |

---

## Project Overview

We applied CRISP-DM to the [Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis) dataset (~2 240 customers, 29 raw features) with two goals:

| Goal | Task | Best Result |
|------|------|-------------|
| **1** | Binary classification — predict campaign response (`Response`) | Logistic Regression — **89.2 % accuracy, AUC 0.912** |
| **2** | Unsupervised clustering — discover customer personas | K-Means (k = 4) on Autoencoder latent space + DEC |

---

## Repository Structure

```
.
├── data/
│   ├── marketing_campaign.csv          # Raw dataset
│   ├── cleaned_marketing_campaign.csv  # After cleaning
│   └── customers_featured.csv          # After feature engineering (64 cols)
│
├── 01_Feature_Engineering.ipynb        # RFM, spending ratios, channel shares
├── 02_Exploratory_Data_Analysis.ipynb  # 11 figures + statistical analysis
├── 03_Clustering_Models.ipynb          # Autoencoder + K-Means, DEC
├── 04_Classification_Models.ipynb      # Logistic Regression, Random Forest, Deep NN
├── 05_Model_Evaluation.ipynb           # Cross-model comparison & interpretation
│
├── reports/
│   ├── figs/                           # EDA & model figures (PNG)
│   └── tables/                         # Feature dictionary, MI scores, heatmap
│
├── results_lr/                         # Logistic Regression outputs
├── results_rf/                         # Random Forest outputs
├── results_dl/                         # Deep Learning outputs
│
├── docs/                               # Course report & presentation slides
├── requirements.txt
└── LICENSE
```

---

## Methodology

### 1 — Feature Engineering (Notebook 01)

Starting from the cleaned dataset, we built ~40 features grouped into:

- **RFM scores** — Recency, Frequency (purchases/month), Monetary (log-scaled)
- **Spending ratios** — share per product category (Wines, Meat, Gold, Fruits, etc.)
- **Channel preferences** — Web / Store / Catalog / Deals share
- **Campaign history** — `Campaign_Accept_Rate`, `Ever_Accepted_Past`, `Past_Accepted`
- **Demographics** — `Customer_Tenure_Days`, `Age`, `Income_per_Capita`, `Spend_per_Capita`
- **Interaction terms** — `Age_x_WebShare`, `Premium_Tilt`, `Category_Concentration`

### 2 — Exploratory Data Analysis (Notebook 02)

Key findings across 11 figures (saved in `reports/figs/`):

- Response rate is ~14.9 % — class imbalance handled in modelling
- Income and total spending are the strongest univariate predictors
- Customers who accepted past campaigns are 5x more likely to respond again
- Channel-preference clusters are visible in PCA space

### 3 — Clustering (Notebook 03)

Two deep-learning based clustering approaches:

| Method | Description |
|--------|-------------|
| **Autoencoder + K-Means** | 3-layer encoder (64 → 32 → 10) then K-Means in latent space (k = 4) |
| **Deep Embedded Clustering (DEC)** | End-to-end soft-assignment refinement on the encoder |

Four customer personas emerged:
- **High-Value Loyalists** — high income, high spend, multi-channel, accepted past campaigns
- **Established Mid-Tier** — moderate income, prefer in-store, moderate response
- **Young Budget Shoppers** — lower income, deal-driven, low response
- **Occasional Buyers** — low frequency, web-only, youngest segment

### 4 — Classification (Notebook 04)

| Model | Accuracy | AUC |
|-------|----------|-----|
| Logistic Regression | **89.2 %** | **0.912** |
| Random Forest | **89.2 %** | 0.882 |
| Deep Logistic (NN) | 84.9 % | 0.500 * |
| Deep RF Equivalent (NN) | 84.9 % | 0.500 * |

\* Deep models suffered from class imbalance (no SMOTE/class-weight tuning in the DL branch).

**Top predictive features (RF importance):** Recency, Campaign_Accept_Rate, Customer_Tenure_Days, Spend_per_Capita, Past_Accepted.

### 5 — Model Evaluation (Notebook 05)

- Confusion matrices, ROC curves, classification reports for all models
- Feature importance comparison (LR coefficients vs. RF Gini importance)
- Discussion of class imbalance impact and possible improvements

---

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the pipeline locally

Run the notebooks in order (01 → 05) in JupyterLab or VS Code. Each notebook reads outputs from the previous one. Alternatively:

```bash
jupyter nbconvert --to notebook --execute 01_Feature_Engineering.ipynb
jupyter nbconvert --to notebook --execute 02_Exploratory_Data_Analysis.ipynb
jupyter nbconvert --to notebook --execute 03_Clustering_Models.ipynb
jupyter nbconvert --to notebook --execute 04_Classification_Models.ipynb
jupyter nbconvert --to notebook --execute 05_Model_Evaluation.ipynb
```

### Run with Prefect (local)

To run the pipeline with Prefect orchestration locally:

```bash
python pipeline.py
```

This will execute all 5 notebooks in sequence using `papermill`, with automatic retry on failure.

---

## Prefect Cloud Deployment

This pipeline can be deployed to **Prefect Cloud** for scheduled, monitored execution in the cloud.

### Quick start

1. **Create a free account**: [cloud.prefect.io](https://cloud.prefect.io)
2. **Authenticate**: `uvx prefect-cloud login`
3. **Deploy**: See [DEPLOY_PREFECT_CLOUD.md](DEPLOY_PREFECT_CLOUD.md) for full instructions

### Example: Deploy & schedule

```bash
# Deploy
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <your-github-username>/Customer-Personality-Analysis \
    --name customer-analysis-pipeline

# Run manually
uvx prefect-cloud run customer_personality_pipeline/customer-analysis-pipeline

# Schedule daily at midnight
uvx prefect-cloud schedule customer_personality_pipeline/customer-analysis-pipeline "0 0 * * *"
```

**Features:**
- ✅ Automatic retry on failure (max 1 retry, 30–60s backoff)
- ✅ Real-time logs in the Prefect Cloud dashboard
- ✅ Email/Slack notifications on success or failure
- ✅ Version control integration (auto-pull from GitHub)
- ✅ Parameterizable runs (override model hyperparameters at runtime)

See [DEPLOY_PREFECT_CLOUD.md](DEPLOY_PREFECT_CLOUD.md) for full deployment guide and troubleshooting.

---

## Selected Figures

| Figure | Description |
|--------|-------------|
| `fig00_response_distribution.png` | Target class distribution |
| `fig06_income_spending_response.png` | Income vs. spending, coloured by response |
| `fig07_correlation_matrix.png` | Feature correlation heatmap |
| `fig10_rfm_resp_heatmap.png` | RFM bins vs. mean response rate |
| `fig11_mutual_information.png` | Mutual information ranking |

---

## Tech Stack

| Library | Usage |
|---------|-------|
| pandas, numpy | Data manipulation |
| scikit-learn | Preprocessing, Logistic Regression, Random Forest, evaluation |
| TensorFlow / Keras | Autoencoder, DEC, deep neural networks |
| matplotlib, seaborn | Visualisation |
| joblib | Model serialisation |

---

## Data

The raw dataset is included for reproducibility.  
Source: [Kaggle — Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)  
License: Community Data License Agreement — Sharing, Version 1.0.

---

## License

This project is released under the MIT License — see [LICENSE](LICENSE) for details.
