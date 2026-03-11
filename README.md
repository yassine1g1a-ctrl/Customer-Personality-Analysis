# Customer Personality Analysis — D7043E Advanced Data Mining

> End-to-end data mining pipeline for customer segmentation and marketing campaign response prediction.  
> Built as part of the course **D7043E – Advanced Data Mining** at Luleå University of Technology (LTU).

---

## 📌 Project Overview

This project applies a full **CRISP-DM** methodology to the [Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis) dataset (~2 240 customers, 29 features) with two primary goals:

| Goal | Task | Best Result |
|------|------|-------------|
| **1** | Binary classification — predict whether a customer accepts the next campaign (`Response`) | Logistic Regression · **89.2 % accuracy · AUC 0.912** |
| **2** | Unsupervised clustering — discover customer personas | K-Means (k=4) + Autoencoder + Deep Embedded Clustering (DEC) |

---

## 🗂️ Repository Structure

```
├── marketing_campaign.csv          # Raw dataset (source)
├── cleaned_marketing_campaign.csv  # After data cleaning
├── customers_featured.csv          # After feature engineering
│
├── 03_Feature_Engineering.ipynb    # RFM + behavioural feature construction
├── 04_Exploratory_Data_Analysis.ipynb  # 11 figures, statistical insights
├── 05_Clustering_Models.ipynb      # Autoencoder + K-Means · DEC
├── 07_Classification model.ipynb   # Logistic Regression · Random Forest · Deep NN
├── 08_Model_Evaluation.ipynb       # Cross-model comparison & interpretation
│
├── reports/
│   ├── figs/                       # All EDA & model figures (PNG)
│   └── tables/                     # Feature dictionary, MI scores, RFM heatmap
│
├── results_lr/                     # Logistic Regression artefacts & metrics
├── results_rf/                     # Random Forest artefacts & metrics
├── results_dl/                     # Deep learning artefacts & metrics
│
└── requirements.txt
```

---

## 🔬 Methodology

### 1 · Feature Engineering (`03`)
Starting from the cleaned dataset, the following feature families were constructed:

- **RFM scores** — Recency, Frequency (purchases/month), Monetary (log-scaled)
- **Spending ratios** — share per product category (Wine, Meat, Gold, Fruits …)
- **Channel preferences** — Web / Store / Catalog / Deals share
- **Campaign history** — `Campaign_Accept_Rate`, `Ever_Accepted_Past`, `Past_Accepted`
- **Demographics** — `Customer_Tenure_Days`, `Age`, `Income_per_Capita`, `Spend_per_Capita`
- **Interaction terms** — `Age_x_WebShare`, `Premium_Tilt`, `Category_Concentration`

### 2 · Exploratory Data Analysis (`04`)
Key findings (11 figures saved in `reports/figs/`):

- Response rate is **~14.9 %** (class imbalance addressed in models)
- Income and total spending are the strongest univariate predictors
- Customers who accepted past campaigns are 5× more likely to respond
- Clear channel-preference clusters visible in PCA space

### 3 · Clustering (`05`)
Two deep-learning clustering approaches:

| Method | Description |
|--------|-------------|
| **Autoencoder + K-Means** | 3-layer encoder (64→32→10) → latent K-Means (k=4) |
| **Deep Embedded Clustering (DEC)** | End-to-end soft-assignment refinement on the encoder |

Four interpretable customer personas were identified:
- 🏆 **High-Value Loyalists** — high income, high spend, multi-channel, accepted past campaigns
- 💼 **Established Mid-Tier** — moderate income, prefer in-store, moderate response
- 🧑‍🎓 **Young Budget Shoppers** — lower income, deal-driven, low response
- 🛒 **Occasional Buyers** — low frequency, web-only, youngest segment

### 4 · Classification (`07`)

| Model | Accuracy | AUC |
|-------|----------|-----|
| Logistic Regression | **89.2 %** | **0.912** |
| Random Forest | **89.2 %** | 0.882 |
| Deep Logistic (NN) | 84.9 % | 0.500 * |
| Deep RF Equivalent (NN) | 84.9 % | 0.500 * |

> \* Deep models affected by class imbalance; no SMOTE/class-weight applied in the DL branch.

**Top predictive features (Random Forest importance):**
`Recency` · `Campaign_Accept_Rate` · `Customer_Tenure_Days` · `Spend_per_Capita` · `Past_Accepted`

### 5 · Model Evaluation (`08`)
- Confusion matrices, ROC curves, and classification reports for all models
- Feature-importance comparison between LR coefficients and RF Gini importance
- Discussion of class imbalance impact and mitigation strategies

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the pipeline in order
```bash
# 1. Feature engineering (produces customers_featured.csv)
jupyter nbconvert --to notebook --execute 03_Feature_Engineering.ipynb

# 2. EDA (produces figures in reports/figs/)
jupyter nbconvert --to notebook --execute 04_Exploratory_Data_Analysis.ipynb

# 3. Clustering
jupyter nbconvert --to notebook --execute 05_Clustering_Models.ipynb

# 4. Classification
jupyter nbconvert --to notebook --execute "07_Classification model.ipynb"

# 5. Evaluation
jupyter nbconvert --to notebook --execute 08_Model_Evaluation.ipynb
```

Or simply open each notebook in **JupyterLab / VS Code** and run cells top-to-bottom.

---

## 📊 Key Figures

| Figure | Description |
|--------|-------------|
| `fig00_response_distribution.png` | Target class imbalance |
| `fig06_income_spending_response.png` | Income vs. spending coloured by Response |
| `fig07_correlation_matrix.png` | Feature correlation heatmap |
| `fig10_rfm_resp_heatmap.png` | RFM × Response interaction |
| `fig11_mutual_information.png` | Mutual information scores per feature |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?logo=scikit-learn)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)

| Library | Usage |
|---------|-------|
| `pandas` / `numpy` | Data manipulation |
| `scikit-learn` | ML pipelines, LR, RF, metrics |
| `tensorflow` / `keras` | Autoencoder, DEC, Deep NN |
| `matplotlib` / `seaborn` | Visualisation |
| `joblib` | Model serialisation |

---

## 📁 Data

The raw dataset is included in this repository for reproducibility.  
Original source: [Kaggle — Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)  
License: Community Data License Agreement – Sharing, Version 1.0.

---

## 📄 License

This project is released under the **MIT License** — see [LICENSE](LICENSE) for details.
