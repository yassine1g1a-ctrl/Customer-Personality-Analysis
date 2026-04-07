# REDEPLOY NOW (Quick Guide)

The fix is ready. Two changes were made:

✅ **prefect.yaml** — Fixed: `git_clone` now runs BEFORE `run_shell_script`  
✅ **pipeline.py** — Added: Auto-fallback to install missing packages

## Command (Copy-Paste)

Replace `<USERNAME>` with your GitHub username:

```bash
git add .
git commit -m "Fix: correct prefect.yaml pull step order + auto-install fallback"
git push origin main

uvx prefect-cloud login
uvx prefect-cloud delete customer_personality_pipeline/customer-analysis-pipeline
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from <USERNAME>/Customer-Personality-Analysis \
    --name customer-analysis-pipeline \
    --python-version 3.12

uvx prefect-cloud run customer_personality_pipeline/customer-analysis-pipeline
```

## Example

If your GitHub username is `john-doe`:

```bash
git add .
git commit -m "Fix: correct prefect.yaml pull step order + auto-install fallback"
git push origin main

uvx prefect-cloud login
uvx prefect-cloud delete customer_personality_pipeline/customer-analysis-pipeline
uvx prefect-cloud deploy pipeline.py:customer_personality_pipeline \
    --from john-doe/Customer-Personality-Analysis \
    --name customer-analysis-pipeline \
    --python-version 3.12

uvx prefect-cloud run customer_personality_pipeline/customer-analysis-pipeline
```

## Expected Output

```
✓ All deployment steps completed successfully
(Runs for ~5-10 minutes)
✓ Flow completed successfully
```

Monitor at: https://cloud.prefect.io → Runs

---

## Notes

- The `{{ GITHUB_USER }}` and `{{ REPO_NAME }}` variables in `prefect.yaml` should be automatically replaced by Prefect based on the `--from` flag.
- **If deployment fails** with "repository not found" or URL issues, run this first:
  ```bash
  python fix_prefect_yaml.py <USERNAME> Customer-Personality-Analysis
  git add prefect.yaml
  git commit -m "Fill in prefect.yaml variables"
  git push origin main
  ```
  Then redeploy.
- The auto-install fallback in `pipeline.py` ensures packages are installed even if the bash script fails.

**Need help?** Check [FIX_DEPLOYMENT_ERROR.md](FIX_DEPLOYMENT_ERROR.md) for troubleshooting.
