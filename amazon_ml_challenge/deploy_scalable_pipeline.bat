@echo off
REM ============================================================
REM deploy_scalable_pipeline.bat
REM Deploys the scalable pipeline (handles 2.2M+ records).
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM Run AFTER: fix_python_and_install.bat succeeded
REM ============================================================

echo.
echo ====================================================
echo  DEPLOYING SCALABLE PIPELINE
echo  Replacing files that cannot handle 2M+ records
echo ====================================================
echo.

REM --- 1. Replace blocker.py ---
echo [1/5] Updating blocker.py (scalable chunked version)...
copy /Y "blocker_scalable.py" "code\business_entity_resolution\src\blocker.py"
if errorlevel 1 (echo   ERROR: could not copy blocker_scalable.py & pause & exit /b 1)
echo       OK.

REM --- 2. Replace run_pipeline.py ---
echo [2/5] Updating run_pipeline.py (scalable version)...
copy /Y "run_pipeline_scalable.py" "code\business_entity_resolution\src\run_pipeline.py"
if errorlevel 1 (echo   ERROR: could not copy run_pipeline_scalable.py & pause & exit /b 1)
echo       OK.

REM --- 3. Replace config.py (dataclass) ---
echo [3/5] Updating config.py (new fields for scalable pipeline)...
copy /Y "config_updated.py" "code\business_entity_resolution\src\config.py"
if errorlevel 1 (echo   ERROR: could not copy config_updated.py & pause & exit /b 1)
echo       OK.

REM --- 4. Replace configs/config.yaml ---
echo [4/5] Updating configs\config.yaml (tuned for large dataset)...
copy /Y "config_scalable.yaml" "configs\config.yaml"
if errorlevel 1 (echo   ERROR: could not copy config_scalable.yaml & pause & exit /b 1)
echo       OK.

REM --- 5. Create required folders ---
echo [5/5] Creating cache directories...
if not exist "models"                            mkdir models
if not exist "models\blocking_cache"             mkdir models\blocking_cache
if not exist "models\blocking_cache\normalized"  mkdir models\blocking_cache\normalized
if not exist "output"                            mkdir output
echo       OK.

REM --- Verify the deployed files ---
echo.
echo --- Verifying deployment ---
if exist "code\business_entity_resolution\src\blocker.py"      (echo   [OK] blocker.py) else (echo   [MISSING] blocker.py)
if exist "code\business_entity_resolution\src\run_pipeline.py" (echo   [OK] run_pipeline.py) else (echo   [MISSING] run_pipeline.py)
if exist "code\business_entity_resolution\src\config.py"       (echo   [OK] config.py) else (echo   [MISSING] config.py)
if exist "configs\config.yaml"                                  (echo   [OK] configs\config.yaml) else (echo   [MISSING] configs\config.yaml)

echo.
echo ====================================================
echo  Scalable pipeline deployed successfully!
echo.
echo  NEXT STEP:
echo    Double-click  run_train_venv.bat
echo    (Takes 2-4 hours - keep laptop plugged in)
echo.
echo  If training crashes midway - just re-run it.
echo  All intermediate results are cached to disk.
echo ====================================================
echo.
pause
