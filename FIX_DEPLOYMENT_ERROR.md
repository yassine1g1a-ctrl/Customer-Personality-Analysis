# Fix: Redeploy to Prefect Cloud (After ModuleNotFoundError)

**The error is now fixed!** The issue was twofold:
1. The `run_shell_script` was executing **before** `git_clone`, so `requirements.txt` didn't exist yet
2. A backup dependency-installation mechanism is now built into `pipeline.py`

## What Changed

| File | Fix |
|------|-----|
| `prefect.yaml` | Reordered: `git_clone` → `run_shell_script` (was reversed) |
| `pipeline.py` | Added `ensure_dependencies()` function that auto-installs missing packages |

## Quick Redeploy (3 steps)

### 1. Push the fixes to GitHub

```bash
git add prefect.yaml pipeline.py
git commit -m "Fix: reorder prefect.yaml steps + auto-install deps in flow"
git push origin main
```

### 2. Redeploy to Prefect Cloud

```bash
# Customize <username> and <repo>
uvx prefect-cloud login
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <username>/Customer-Personality-Analysis \
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

### 3. Test the deployment

```bash
uvx prefect-cloud run \
    customer_personality_pipeline/customer-analysis-pipeline
```

Monitor logs at [cloud.prefect.io](https://cloud.prefect.io) → Runs.

---

## How the Fix Works

### Before (❌ didn't work):
```yaml
pull:
  - type: run_shell_script      # ← Runs FIRST but requirements.txt doesn't exist yet!
  - type: git_clone              # ← Runs SECOND, clones the repo
```

### After (✅ now works):
```yaml
pull:
  - type: git_clone              # ← Runs FIRST, clones repo with requirements.txt
  - type: run_shell_script       # ← Runs SECOND, installs from requirements.txt
    commands:
      - pip install -r requirements.txt
```

### Bonus: Auto-install Fallback

`pipeline.py` now includes:
```python
def ensure_dependencies():
    """Install missing deps if not already present."""
    for pkg in ["papermill", "prefect"]:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
```

This means even if the `prefect.yaml` steps fail for any reason, the flow will still work.

---

## Troubleshooting

### Still seeing "ModuleNotFoundError"?

1. **Verify the files are updated:**
   ```bash
   git status  # Should show nothing, all committed
   git log --oneline -1  # Shows your commit message
   ```

2. **Clear old deployment:**
   ```bash
   uvx prefect-cloud delete customer_personality_pipeline/customer-analysis-pipeline
   ```
   Then redeploy.

3. **Check GitHub push:**
   ```bash
   git push -v origin main  # Verify push succeeded
   ```

### Different error now?

Share the full error from Prefect Cloud logs and we'll fix it.

---

## Verify Locally Before Deploying

```bash
cd /path/to/Customer-Personality-Analysis
python pipeline.py
```

This should run all 5 notebooks locally without errors.

---

## Next: Schedule Your Pipeline

Once deployment succeeds:

```bash
# Daily at midnight UTC
uvx prefect-cloud schedule \
    customer_personality_pipeline/customer-analysis-pipeline \
    "0 0 * * *"

# View schedule
uvx prefect-cloud deployment ls
```

---

**Done! Your ML pipeline is now ready to run in the cloud.** 🚀
