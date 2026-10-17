@echo off
echo.
echo ====================================================
echo  VALIDATING OUTPUT FILES
echo  You MUST see PASS before uploading to Unstop.
echo ====================================================
echo.
cd /d %~dp0
call venv\Scripts\activate.bat
python code\business_entity_resolution\utils\validate_submission.py ^
    --matching output\matching_results.tsv ^
    --candidate output\candidate_pairs.tsv ^
    --test-dir dataset\test
echo.
echo If you see PASS: upload output\matching_results.tsv to Unstop portal.
echo If you see errors: screenshot them and ask Claude to fix.
echo.
pause
