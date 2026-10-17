@echo off
echo.
echo ====================================================
echo  GENERATING PREDICTIONS ON TEST SET
echo  Takes 30-90 minutes.
echo ====================================================
echo.
cd /d %~dp0
call venv\Scripts\activate.bat
python code\business_entity_resolution\src\run_pipeline.py --mode predict --config configs\config.yaml
echo.
echo Done! Files created:
echo   output\matching_results.tsv  ^<-- UPLOAD THIS to Unstop
echo   output\candidate_pairs.tsv   ^<-- needed for final zip
echo.
echo Next: run run_validate_venv.bat before uploading.
echo.
pause
