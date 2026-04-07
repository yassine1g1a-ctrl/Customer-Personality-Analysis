# Fix: NoSuchKernel('python3') Error

**Error resolved:** `jupyter_client.kernelspec.NoSuchKernel: No such kernel named python3`

## What Changed

✅ **pipeline.py:**
- Enhanced `ensure_dependencies()` to automatically **register the Python kernel** with Jupyter using `ipykernel`
- Removed `kernel_name="python3"` from all 5 `pm.execute_notebook()` calls (let papermill auto-detect)

✅ **requirements.txt:**
- Already includes `ipykernel>=6.0` and `jupyter>=1.0`

---

## Quick Redeploy

```bash
# 1. Push the fix
git add pipeline.py
git commit -m "Fix: auto-register Python kernel + remove explicit kernel_name"
git push origin main

# 2. Redeploy
uvx prefect-cloud delete customer_personality_pipeline/customer-analysis-pipeline
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <USERNAME>/Customer-Personality-Analysis \
    --name customer-analysis-pipeline \
    --python-version 3.12

# 3. Run
uvx prefect-cloud run customer_personality_pipeline/customer-analysis-pipeline
```

---

## How It Works

1. **On startup**, `ensure_dependencies()` runs before any imports
2. **Installs** missing packages: `papermill`, `prefect`, `ipykernel`, `jupyter`
3. **Registers** the Python kernel with Jupyter: `python -m ipykernel install --user --name python3`
4. **Notebooks execute** with papermill, which now finds the registered kernel

---

**Expected behavior:** Flow should run successfully and process all 5 notebooks.
