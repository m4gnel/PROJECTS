# GitHub Setup Guide
# Amazon ML Challenge 2026

## Step 1 — Create a GitHub Account (if you don't have one)
Go to https://github.com and sign up. It's free.

## Step 2 — Install Git on Windows
Download from: https://git-scm.com/download/win
Click through the installer with all default options.
After install, open a new Command Prompt and test:
```
git --version
```
You should see something like: git version 2.45.0

## Step 3 — Create a New Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `amazon-ml-challenge-2026`
3. Set to **Private** (competition code should stay private)
4. Do NOT initialize with README (we already have one)
5. Click "Create repository"
6. Copy the URL shown (looks like: https://github.com/YourName/amazon-ml-challenge-2026.git)

## Step 4 — Set Up Git in Your Project Folder
Open Command Prompt, navigate to your project:
```
cd D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE
```

Then run these commands ONE BY ONE:
```
git init
git add .
git commit -m "Initial commit - Amazon ML Challenge 2026 pipeline"
git branch -M main
git remote add origin https://github.com/YourName/amazon-ml-challenge-2026.git
git push -u origin main
```

Replace `YourName` with your actual GitHub username.

## Step 5 — Copy .gitignore File
Before the `git add .` command above, rename `gitignore.txt` to `.gitignore`:
```
rename gitignore.txt .gitignore
```
This prevents large files (dataset, models) from being uploaded to GitHub.

## What Gets Uploaded to GitHub (Safe)
- All code in code/
- All brain docs in brain/
- configs/ files
- notebooks/ scripts
- README, Makefile, bat files
- requirements.txt

## What Does NOT Get Uploaded (Blocked by .gitignore)
- dataset/ folder (competition data - keep private)
- models/ folder (large pkl files)
- output/ files
- __MACOSX/ junk

## Step 6 — Daily Workflow After Setup
When you make changes and want to save them to GitHub:
```
git add .
git commit -m "Describe what you changed"
git push
```

## Step 7 — If You Have a Teammate
They can clone your repo:
```
git clone https://github.com/YourName/amazon-ml-challenge-2026.git
```
Then they need to: download dataset separately (never put it on GitHub), run install.bat, and they're ready.

## VS Code GitHub Integration (Optional, Easier)
If you use VS Code:
1. Install the "GitHub Pull Requests" extension
2. Press Ctrl+Shift+P → "Git: Initialize Repository"
3. Click the Source Control icon (branch icon on left sidebar)
4. Stage all files → write commit message → click Commit → Push

This gives you a visual interface instead of command line.
