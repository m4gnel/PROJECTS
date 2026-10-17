@echo off
echo.
echo ====================================================
echo  TRAINING THE MODEL
echo  Takes 2-4 hours. Keep laptop plugged in.
echo  Do NOT close this window.
echo  If it crashes: just re-run - it resumes from cache.
echo ====================================================
echo.
cd /d %~dp0
call venv\Scripts\activate.bat
python code\business_entity_resolution\src\run_pipeline.py --mode train --config configs\config.yaml
echo.
echo Training finished. Check the score printed above.
echo Target: Macro F0.5 above 0.85 (higher is better).
echo.
echo Next step: run run_predict_venv.bat
echo.
pause
