@echo off
REM ============================================================
REM install.bat
REM Run this from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM Installs all Python libraries needed for the pipeline
REM ============================================================

echo.
echo ====================================================
echo  Installing Python dependencies...
echo  This will take 5-15 minutes (downloads ~2GB)
echo  DO NOT CLOSE THIS WINDOW
echo ====================================================
echo.

REM Check Python is available
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during install
    pause
    exit /b 1
)

echo.
echo Installing libraries...
pip install pandas==2.2.2
pip install numpy==1.26.4
pip install scikit-learn==1.5.1
pip install rapidfuzz==3.9.6
pip install lightgbm==4.4.0
pip install scipy==1.13.1
pip install joblib==1.4.2
pip install pyyaml==6.0.1
pip install pytest==8.2.2
pip install tqdm==4.66.4
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers==3.0.1
pip install transformers==4.42.4

echo.
echo ====================================================
echo  Installation complete!
echo  Next: Run run_eda.bat to analyze data
echo ====================================================
echo.
pause
