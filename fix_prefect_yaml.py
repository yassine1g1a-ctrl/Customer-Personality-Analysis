#!/usr/bin/env python3
"""
Fix prefect.yaml variables if they weren't replaced automatically.
Run this BEFORE deploying if variables {{ GITHUB_USER }} and {{ REPO_NAME }} weren't replaced.

Usage:
    python fix_prefect_yaml.py <github-username> <repo-name>
    
Example:
    python fix_prefect_yaml.py john-doe Customer-Personality-Analysis
"""

import sys
import os

def fix_prefect_yaml(github_user: str, repo_name: str):
    path = "prefect.yaml"
    
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        sys.exit(1)
    
    with open(path, "r") as f:
        content = f.read()
    
    # Replace variables
    original = content
    content = content.replace("{{ GITHUB_USER }}", github_user)
    content = content.replace("{{ REPO_NAME }}", repo_name)
    
    if original == content:
        print(f"✓ No variables to replace (already correct)")
        sys.exit(0)
    
    with open(path, "w") as f:
        f.write(content)
    
    print(f"✓ Updated prefect.yaml:")
    print(f"  Repository: https://github.com/{github_user}/{repo_name}")
    print(f"\nNext step:")
    print(f"  git add prefect.yaml")
    print(f"  git commit -m 'Fill in prefect.yaml variables'")
    print(f"  git push origin main")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    fix_prefect_yaml(sys.argv[1], sys.argv[2])
