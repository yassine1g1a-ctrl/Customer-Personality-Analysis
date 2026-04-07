# Deploying to Prefect Cloud

This guide explains how to deploy and run your ML pipeline on Prefect Cloud.

## Prerequisites

- **Prefect account**: Free account at [cloud.prefect.io](https://cloud.prefect.io)
- **GitHub repository**: Push your code to GitHub
- **`uv` installed**: See [astral-sh/uv](https://github.com/astral-sh/uv)
- **GitHub Personal Access Token**: For accessing your private repo (optional, required if repo is private)

## Step-by-Step Deployment

### 1. Login to Prefect Cloud

```bash
uvx prefect-cloud login
```

This stores your API key locally at `~/.prefect/profiles.toml`.

### 2. Connect Your GitHub Account

```bash
uvx prefect-cloud github setup
```

This grants Prefect permission to clone your GitHub repositories.

### 3. Push Your Code (if not already done)

Ensure your repository includes:
- `pipeline.py`
- `prefect.yaml`
- `requirements.txt`
- All 5 notebooks (`01_*.ipynb` through `05_*.ipynb`)
- `data/` directory (or data stays in your Cloud storage)

```bash
git add .
git commit -m "Add Prefect pipeline"
git push origin main
```

### 4. Deploy the Flow

**Update the repository path in the following command:**

```bash
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <github-username>/<repository-name> \
    --name customer-analysis-pipeline \
    --python-version 3.12
```

**Example:**

```bash
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from john-doe/Customer-Personality-Analysis \
    --name customer-analysis-pipeline \
    --python-version 3.12
```

### 5. Run Your Flow (Manual Trigger)

```bash
uvx prefect-cloud run \
    customer_personality_pipeline/customer-analysis-pipeline
```

**With parameter overrides:**

```bash
uvx prefect-cloud run \
    customer_personality_pipeline/customer-analysis-pipeline \
    --param "random_seed=123" \
    --param "n_clusters=4" \
    --param "dl_epochs=100"
```

### 6. Schedule Your Flow

**Daily at midnight UTC:**

```bash
uvx prefect-cloud schedule \
    customer_personality_pipeline/customer-analysis-pipeline \
    "0 0 * * *"
```

**Hourly:**

```bash
uvx prefect-cloud schedule \
    customer_personality_pipeline/customer-analysis-pipeline \
    "0 * * * *"
```

**Every Monday at 9 AM UTC:**

```bash
uvx prefect-cloud schedule \
    customer_personality_pipeline/customer-analysis-pipeline \
    "0 9 * * 1"
```

### 7. Monitor Your Runs

Visit the [Prefect Cloud dashboard](https://cloud.prefect.io) to:
- View run logs in real time
- Track task execution times
- See failed runs and retry attempts
- Manage schedules

---

## Understanding the Deployment Flow

The `prefect.yaml` file configures:

1. **Pull step**: Clones your GitHub repo into the runner environment
2. **Dependencies**: Installs `pip install -r requirements.txt`
3. **Entrypoint**: Specifies which flow to run (`pipeline.py:customer_personality_pipeline`)

When a run is triggered, Prefect:
1. Clones your repo at the specified branch
2. Installs Python dependencies
3. Executes `pipeline.py:customer_personality_pipeline`
4. Runs tasks **1 → 2 → 3 → 4 → 5** in sequence
5. Retries failed tasks automatically (max 1 retry, 30–60s delay)
6. Logs all output to the dashboard

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'papermill'"

**Cause**: Dependencies were not installed in the cloud environment.

**Fix**: Ensure `prefect.yaml` exists and includes:
```yaml
pull:
  - type: run_shell_script
    commands:
      - pip install -r requirements.txt
```

Then redeploy:
```bash
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <your-repo> \
    --name customer-analysis-pipeline
```

### "repository not found" or "authentication failed"

**Cause**: GitHub token missing or repo is private.

**Fix**: For private repos, create a GitHub Personal Access Token:
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Select `repo` scope
4. Copy the token
5. Set environment variable:
   ```bash
   $env:PREFECT_GITHUB_TOKEN = "ghp_xxxxx"
   ```
6. Redeploy

---

## Local Testing (Before Cloud Deployment)

Test locally before deploying to ensure everything works:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline locally
python pipeline.py
```

Output notebooks will be saved as `*_output.ipynb` in the repo directory.

---

## Managing Deployments

### View all deployments

```bash
uvx prefect-cloud deployment ls
```

### Remove a schedule

```bash
uvx prefect-cloud unschedule \
    customer_personality_pipeline/customer-analysis-pipeline
```

### Delete a deployment

```bash
uvx prefect-cloud delete \
    customer_personality_pipeline/customer-analysis-pipeline
```

---

## Pipeline Parameters

You can override parameters when deploying or running:

```bash
# Set at run time
uvx prefect-cloud run \
    customer_personality_pipeline/customer-analysis-pipeline \
    --param "random_seed=999" \
    --param "dl_epochs=200" \
    --param "n_clusters=6"
```

Available parameters:
- `random_seed` (int): Reproducibility seed
- `n_clusters` (int): Number of customer personas (default: 5)
- `dl_epochs` (int): Deep learning epochs (default: 70)
- `dl_rf_epochs` (int): Deep RF epochs (default: 150)
- `test_size` (float): Train/test split ratio (default: 0.2)
- `rf_n_estimators` (int): Random Forest trees (default: 200)

See `pipeline.py` for the full parameter list.

---

## Next Steps

- **Customize parameters** at the flow level (in `pipeline.py`)
- **Add alerting**: Configure Slack notifications on task failure
- **Scale compute**: Use custom Work Pools for GPU/larger instances
- **Version your models**: Archive trained models with timestamps
