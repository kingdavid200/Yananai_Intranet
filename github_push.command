#!/bin/bash
cd "$(dirname "$0")"

echo "=== Project Yananai — GitHub Setup ==="
echo ""

# Check for gh CLI
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) not found."
    echo "Install it from: https://cli.github.com"
    echo "Then run: gh auth login"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Check if already logged in
if ! gh auth status &> /dev/null; then
    echo "Not logged in to GitHub CLI. Running login..."
    gh auth login
fi

# Get GitHub username
GH_USER=$(gh api user --jq '.login')
echo "Logged in as: $GH_USER"
echo ""

REPO_NAME="yananai-intranet"
REPO_FULL="$GH_USER/$REPO_NAME"

# Create GitHub repo (private)
echo "Creating private GitHub repo: $REPO_FULL ..."
gh repo create "$REPO_NAME" \
    --private \
    --description "Project Yananai Staff Intranet" \
    2>&1

if [ $? -ne 0 ]; then
    echo ""
    echo "Repo may already exist — continuing with push..."
fi

# Init git if not already
if [ ! -d ".git" ]; then
    echo "Initialising git repository..."
    git init
    git branch -M main
fi

# Stage and commit
echo "Staging all files..."
git add .
git status

echo ""
echo "Creating initial commit..."
git commit -m "Initial commit — Project Yananai Intranet

Production-ready Django 6 staff intranet with:
- Full redesign (dark sidebar, brand purple #574A9E)
- Accounts, Directory, Documents, News, Projects apps
- WhiteNoise static files, dj-database-url PostgreSQL support
- Configured for Railway deployment"

# Set remote
REMOTE_URL="https://github.com/$REPO_FULL.git"
echo ""
echo "Setting remote origin to: $REMOTE_URL"
git remote remove origin 2>/dev/null
git remote add origin "$REMOTE_URL"

# Push
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "====================================="
echo "SUCCESS! Repo is live at:"
echo "https://github.com/$REPO_FULL"
echo "====================================="
echo ""
read -p "Press Enter to close..."
