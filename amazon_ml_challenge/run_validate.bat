@echo off
REM ============================================================
REM run_validate.bat - Validate output files before submitting
REM Run from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM NEVER submit without seeing PASS here first.
REM ============================================================
echo.
echo ====================================================
echo  VALIDATING SUBMISSION FILES
echo  You must see PASS before uploading to leaderboard.
echo ====================================================
echo.
python code\business_entity_resolution\utils\validate_submission.py ^
    --matching output\matching_results.tsv ^
    --candidate output\candidate_pairs.tsv ^
    --test-dir dataset\test
echo.
echo If you see PASS above:
echo   Upload output\matching_results.tsv to Unstop portal
echo.
echo If you see errors:
echo   Screenshot them and ask Claude what to fix
echo.
pause
