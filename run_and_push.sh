#!/bin/bash
set -e

echo "Starting Groww Pulse Agent on Railway..."

# 1. Recreate the GCP service account from the environment variable
if [ -n "$GCP_SERVICE_ACCOUNT" ]; then
    echo "Injecting GCP Service Account..."
    echo "$GCP_SERVICE_ACCOUNT" > service_account.json
    export GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
fi

# 2. Run the Python pipeline
echo "Running Python Pipeline..."
PYTHONPATH=. python src/main.py --product Groww --draft-only false

# 3. Commit and push the new data.json back to GitHub
if [ -n "$GITHUB_PAT" ]; then
    echo "Configuring git..."
    git config --global user.email "railway-bot@users.noreply.github.com"
    git config --global user.name "Railway Cron Bot"
    
    # Update the git origin to use the Personal Access Token for authentication
    git remote set-url origin "https://${GITHUB_PAT}@github.com/iamarpit01/weekly-pulse-report.git"
    
    git add frontend/public/data.json
    
    # Only commit and push if there are actual changes
    if ! git diff --staged --quiet; then
        git commit -m "Automated Pulse Report: Update Dashboard Data (Railway) [skip ci]"
        git push origin main
        echo "Successfully pushed fresh data.json to GitHub!"
    else
        echo "No changes in data.json. Skipping push."
    fi
else
    echo "Warning: GITHUB_PAT secret is missing in Railway! Cannot push to GitHub."
fi
