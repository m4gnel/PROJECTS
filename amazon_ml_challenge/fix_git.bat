@echo off
REM ============================================================
REM fix_git.bat
REM Fixes the Git repository problems:
REM   Problem 1: venv/ (42699 files) was accidentally committed
REM   Problem 2: "remote origin already exists" error
REM   Problem 3: junk folders {brain,code and __MACOSX tracked
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM ============================================================

echo.
echo ====================================================
echo  FIXING GIT REPOSITORY
echo  This removes large/junk folders from Git history
echo  and correctly pushes only your code to GitHub.
echo ====================================================
echo.

REM --- STEP 1: Create a proper .gitignore FIRST (before any git operations) ---
echo [1/7] Writing correct .gitignore...
(
echo # ===== NEVER commit these =====
echo.
echo # Python virtual environment (gigabytes, auto-recreated)
echo venv/
echo .venv/
echo env/
echo.
echo # Competition dataset (too large + against fair-play rules)
echo dataset/
echo student_resource/
echo __MACOSX/
echo.
echo # Trained models and cache (large binary files)
echo models/
echo *.pkl
echo *.joblib
echo *.parquet
echo.
echo # Pipeline output files (regenerated each run)
echo output/matching_results.tsv
echo output/candidate_pairs.tsv
echo.
echo # Log files
echo pipeline.log
echo *.log
echo.
echo # Python bytecode
echo __pycache__/
echo *.py[cod]
echo *.pyo
echo.
echo # Junk from bad mkdir command
echo {brain,code/
echo.
echo # Mac metadata files
echo .DS_Store
echo ._*
echo.
echo # Windows thumbnails
echo Thumbs.db
echo desktop.ini
echo.
echo # IDE settings
echo .vscode/settings.json
echo .idea/
echo.
echo # Jupyter checkpoints
echo .ipynb_checkpoints/
) > .gitignore
echo       Done.

REM --- STEP 2: Remove large/wrong folders from Git tracking ---
echo.
echo [2/7] Removing venv/ from Git tracking (stays on disk, removed from GitHub)...
git rm -r --cached venv/ 2>nul
echo       Done (warnings about non-existent files are OK).

echo.
echo [3/7] Removing other ignored folders from Git tracking...
git rm -r --cached student_resource/ 2>nul
git rm -r --cached __MACOSX/ 2>nul
git rm -r --cached models/ 2>nul
git rm -r --cached dataset/ 2>nul
git rm -r --cached "{brain,code" 2>nul
echo       Done.

REM --- STEP 3: Stage only the correct files ---
echo.
echo [4/7] Staging correct project files...
git add .gitignore
git add brain/
git add code/
git add configs/
git add notebooks/
git add output/
git add Documentation_template.md
git add Makefile
git add MASTER_AGENT_PROMPT.md
git add COPILOT_AGENT_PROMPT.md 2>nul
git add GITHUB_SETUP.md 2>nul
git add *.bat 2>nul
git add *.py 2>nul
echo       Done.

REM --- STEP 4: Commit the cleanup ---
echo.
echo [5/7] Committing cleanup...
git commit -m "Fix: remove venv, dataset, junk from tracking; add correct .gitignore"
echo       Done.

REM --- STEP 5: Check current remote ---
echo.
echo [6/7] Checking Git remote...
echo Your current remote:
git remote -v
echo.
REM The remote already exists (from when you ran git remote add before)
REM We just need to push to it

REM --- STEP 6: Push to GitHub ---
echo [7/7] Pushing to GitHub...
echo.
echo If you see a login prompt: enter your GitHub username and password/token.
echo.
git push origin main --force
if errorlevel 1 (
    echo.
    echo Push failed. Trying without --force...
    git push -u origin main
)

echo.
echo ====================================================
echo  Git fix complete!
echo.
echo  What is now ON GitHub (code only):
echo    brain/     - Strategy documents
echo    code/      - All Python source files
echo    configs/   - config.yaml, abbreviations.json
echo    notebooks/ - EDA scripts
echo    *.bat      - Run scripts
echo    README, Makefile
echo.
echo  What is NOT on GitHub (correct - too large/private):
echo    venv/          - Python environment
echo    dataset/       - Competition data
echo    models/        - Trained model files
echo    student_resource/ - Unstop zip contents
echo.
echo  From now on, save code to GitHub with:
echo    git add .
echo    git commit -m "what you changed"
echo    git push
echo ====================================================
echo.
pause
