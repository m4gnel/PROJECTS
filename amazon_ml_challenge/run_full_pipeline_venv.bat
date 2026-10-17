@echo off
echo.
echo ====================================================
echo  RUNNING FULL PIPELINE (TRAIN + PREDICT)
echo  Takes 3-5 hours total. Keep laptop plugged in.
echo  Progress is cached - safe to resume if it crashes.
echo ====================================================
echo.
cd /d %~dp0
call venv\Scripts\activate.bat
python code\business_entity_resolution\src\run_pipeline.py --mode full --config configs\config.yaml
echo.
echo Pipeline complete!
echo Run run_validate_venv.bat before uploading to Unstop.
echo.
pause
