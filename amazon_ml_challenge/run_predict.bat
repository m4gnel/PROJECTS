@echo off
REM ============================================================
REM run_predict.bat - Generate test predictions
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM Takes 5-10 minutes.
REM ============================================================
echo.
echo ====================================================
echo  GENERATING PREDICTIONS ON TEST SET
echo  Takes 5-10 minutes...
echo ====================================================
echo.
python code\business_entity_resolution\src\run_pipeline.py --mode predict --config configs\config.yaml
echo.
echo Done! Files created:
echo   output\matching_results.tsv   (UPLOAD THIS to leaderboard)
echo   output\candidate_pairs.tsv    (needed for final zip)
echo.
echo Next: run run_validate.bat to check files before uploading
echo.
pause
