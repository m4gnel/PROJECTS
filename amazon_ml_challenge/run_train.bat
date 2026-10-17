@echo off
REM ============================================================
REM run_train.bat - Train the AI model
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM Takes 20-60 minutes. DO NOT CLOSE THIS WINDOW.
REM ============================================================
echo.
echo ====================================================
echo  TRAINING THE MODEL
echo  This takes 20-60 minutes. Do not close this window.
echo  You will see progress printed below.
echo ====================================================
echo.
python code\business_entity_resolution\src\run_pipeline.py --mode train --config configs\config.yaml
echo.
echo Training complete! Check the score printed above.
echo If Macro F0.5 is above 0.90 you are in great shape.
echo Next: run run_predict.bat
echo.
pause
