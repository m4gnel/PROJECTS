@echo off
REM ============================================================
REM fix_python_and_install.bat
REM Fixes the Python 3.14 incompatibility issue.
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM ============================================================

echo.
echo ====================================================
echo  FIXING PYTHON VERSION ISSUE
echo  Your Python 3.14 is too new for ML libraries.
echo  We will create a virtual environment that works.
echo ====================================================
echo.

REM --- Check what Python versions are available ---
echo [STEP 1] Checking available Python versions...
echo.

REM Try py launcher (Windows Python launcher - most common)
py --list 2>nul
if errorlevel 1 (
    echo NOTE: py launcher not found, trying direct python commands...
)

echo.
echo Your current Python:
python --version
echo.

REM --- Check if Python 3.11 is already installed ---
echo [STEP 2] Checking for Python 3.11...
py -3.11 --version 2>nul
if not errorlevel 1 (
    echo [FOUND] Python 3.11 is installed!
    goto :create_venv_311
)

REM Check if Python 3.12 is installed
py -3.12 --version 2>nul
if not errorlevel 1 (
    echo [FOUND] Python 3.12 is installed. Using 3.12 instead.
    goto :create_venv_312
)

REM Neither found - need to download
echo.
echo [NOT FOUND] Python 3.11 is not installed.
echo.
echo ====================================================
echo  ACTION REQUIRED: Download Python 3.11
echo ====================================================
echo.
echo  1. Open this link in your browser:
echo     https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
echo.
echo  2. Run the installer
echo  3. IMPORTANT: Check the box "Add Python 3.11 to PATH"  
echo  4. Click "Install Now"
echo  5. After install completes, close this window
echo  6. Open a NEW Command Prompt
echo  7. Run this file again: fix_python_and_install.bat
echo.
echo  The download is about 25 MB and takes 2 minutes to install.
echo.
pause
exit /b 1

:create_venv_311
echo.
echo [STEP 3] Creating virtual environment with Python 3.11...
py -3.11 -m venv venv
goto :activate_and_install

:create_venv_312
echo.
echo [STEP 3] Creating virtual environment with Python 3.12...
py -3.12 -m venv venv
goto :activate_and_install

:activate_and_install
echo.
echo [STEP 4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [STEP 5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [STEP 6] Installing all required packages...
echo          This downloads about 2 GB. Please wait 10-20 minutes.
echo          DO NOT CLOSE THIS WINDOW.
echo.

pip install pandas numpy scikit-learn scipy
pip install rapidfuzz lightgbm joblib pyyaml
pip install tqdm pytest
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers transformers

echo.
echo [STEP 7] Verifying installation...
python -c "import pandas; print('[OK] pandas', pandas.__version__)"
python -c "import numpy; print('[OK] numpy', numpy.__version__)"
python -c "import sklearn; print('[OK] scikit-learn', sklearn.__version__)"
python -c "import scipy; print('[OK] scipy', scipy.__version__)"
python -c "import lightgbm; print('[OK] lightgbm', lightgbm.__version__)"
python -c "import rapidfuzz; print('[OK] rapidfuzz', rapidfuzz.__version__)"
python -c "import sentence_transformers; print('[OK] sentence-transformers', sentence_transformers.__version__)"
python -c "import yaml; print('[OK] pyyaml OK')"

echo.
echo ====================================================
echo  Installation complete!
echo.
echo  IMPORTANT: From now on, ALWAYS use the scripts
echo  that have 'venv' in the name (run_eda_venv.bat etc)
echo  NOT the old bat files.
echo ====================================================
echo.

REM Create new venv-aware bat files
echo Creating new run scripts...

echo @echo off > run_eda_venv.bat
echo call venv\Scripts\activate.bat >> run_eda_venv.bat
echo python notebooks\01_eda.py >> run_eda_venv.bat
echo pause >> run_eda_venv.bat

echo @echo off > run_train_venv.bat
echo call venv\Scripts\activate.bat >> run_train_venv.bat
echo echo Training model - takes 20-60 mins, do not close... >> run_train_venv.bat
echo python code\business_entity_resolution\src\run_pipeline.py --mode train --config configs\config.yaml >> run_train_venv.bat
echo pause >> run_train_venv.bat

echo @echo off > run_predict_venv.bat
echo call venv\Scripts\activate.bat >> run_predict_venv.bat
echo python code\business_entity_resolution\src\run_pipeline.py --mode predict --config configs\config.yaml >> run_predict_venv.bat
echo pause >> run_predict_venv.bat

echo @echo off > run_validate_venv.bat
echo call venv\Scripts\activate.bat >> run_validate_venv.bat
echo python code\business_entity_resolution\utils\validate_submission.py --matching output\matching_results.tsv --candidate output\candidate_pairs.tsv --test-dir dataset\test >> run_validate_venv.bat
echo pause >> run_validate_venv.bat

echo @echo off > run_full_pipeline_venv.bat
echo call venv\Scripts\activate.bat >> run_full_pipeline_venv.bat
echo echo Running FULL pipeline (train + predict)... >> run_full_pipeline_venv.bat
echo python code\business_entity_resolution\src\run_pipeline.py --mode full --config configs\config.yaml >> run_full_pipeline_venv.bat
echo pause >> run_full_pipeline_venv.bat

echo.
echo New scripts created:
echo   run_eda_venv.bat          - Explore the data
echo   run_train_venv.bat        - Train the model
echo   run_predict_venv.bat      - Generate predictions
echo   run_validate_venv.bat     - Validate output files
echo   run_full_pipeline_venv.bat - Train + Predict together
echo.
echo Next step: Double-click run_eda_venv.bat
echo.
pause
