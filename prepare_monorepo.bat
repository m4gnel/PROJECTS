@echo off
title Monorepo Mode: Prepare Projects for Single Repository Upload
echo ========================================================
echo   Configuring Projects for Unified Monorepo Push
echo ========================================================
echo.

powershell -Command "$repos = @('AgriSage\AgriSage', 'Ai_Interview_Coach', 'amazon_ml_challenge', 'flutter-mobile_container', 'J_Code', 'ngo_volunteer_app'); foreach ($r in $repos) { if (Test-Path \"$r\.git\") { Rename-Item -Path \"$r\.git\" -NewName \".git_subrepo\" -Force; Write-Output \"Converted $r to monorepo tracking.\" } }"

echo.
echo Monorepo mode is ACTIVE. All 9 project folders are now fully browsable.
pause
