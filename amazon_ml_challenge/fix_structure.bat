@echo off
REM ============================================================
REM fix_structure.bat
REM Run this from: D:\WORK\PROJECTS\AMAZON_ML_CHALLENGE\
REM Double-click this file OR run in Command Prompt
REM ============================================================

echo.
echo ====================================================
echo  AMAZON ML CHALLENGE - Fixing Folder Structure
echo ====================================================
echo.

REM --- STEP 1: Create dataset folders at root level ---
echo [1/6] Creating dataset folders...
if not exist "dataset" mkdir dataset
if not exist "dataset\train" mkdir dataset\train
if not exist "dataset\test" mkdir dataset\test
echo       Done.

REM --- STEP 2: Copy training data ---
echo [2/6] Copying training data from student_resource...
copy "student_resource\dataset\train\train_source1.tsv" "dataset\train\train_source1.tsv" /Y
copy "student_resource\dataset\train\train_source2.tsv" "dataset\train\train_source2.tsv" /Y
copy "student_resource\dataset\train\train_source3.tsv" "dataset\train\train_source3.tsv" /Y
copy "student_resource\dataset\train\train_ground_truth.tsv" "dataset\train\train_ground_truth.tsv" /Y
echo       Done.

REM --- STEP 3: Copy test data ---
echo [3/6] Copying test data from student_resource...
copy "student_resource\dataset\test\test_source1.tsv" "dataset\test\test_source1.tsv" /Y
copy "student_resource\dataset\test\test_source2.tsv" "dataset\test\test_source2.tsv" /Y
copy "student_resource\dataset\test\test_source3.tsv" "dataset\test\test_source3.tsv" /Y
echo       Done.

REM --- STEP 4: Use official validate_submission.py ---
echo [4/6] Copying official validator...
copy "student_resource\utils\validate_submission.py" "code\business_entity_resolution\utils\validate_submission.py" /Y
echo       Done.

REM --- STEP 5: Delete junk folders ---
echo [5/6] Cleaning junk folders...
if exist "{brain,code" rmdir /S /Q "{brain,code"
if exist "__MACOSX" rmdir /S /Q "__MACOSX"
echo       Done.

REM --- STEP 6: Verify everything is in place ---
echo [6/6] Verifying files...
echo.
echo --- Training files ---
if exist "dataset\train\train_source1.tsv" (echo   [OK] train_source1.tsv) else (echo   [MISSING] train_source1.tsv)
if exist "dataset\train\train_source2.tsv" (echo   [OK] train_source2.tsv) else (echo   [MISSING] train_source2.tsv)
if exist "dataset\train\train_source3.tsv" (echo   [OK] train_source3.tsv) else (echo   [MISSING] train_source3.tsv)
if exist "dataset\train\train_ground_truth.tsv" (echo   [OK] train_ground_truth.tsv) else (echo   [MISSING] train_ground_truth.tsv)

echo.
echo --- Test files ---
if exist "dataset\test\test_source1.tsv" (echo   [OK] test_source1.tsv) else (echo   [MISSING] test_source1.tsv)
if exist "dataset\test\test_source2.tsv" (echo   [OK] test_source2.tsv) else (echo   [MISSING] test_source2.tsv)
if exist "dataset\test\test_source3.tsv" (echo   [OK] test_source3.tsv) else (echo   [MISSING] test_source3.tsv)

echo.
echo --- Code files ---
if exist "code\business_entity_resolution\src\run_pipeline.py" (echo   [OK] run_pipeline.py) else (echo   [MISSING] run_pipeline.py)
if exist "code\business_entity_resolution\utils\validate_submission.py" (echo   [OK] validate_submission.py) else (echo   [MISSING] validate_submission.py)
if exist "configs\config.yaml" (echo   [OK] config.yaml) else (echo   [MISSING] config.yaml)

echo.
echo ====================================================
echo  Structure fix complete!
echo  Next: Run install.bat to install Python libraries
echo ====================================================
echo.
pause
