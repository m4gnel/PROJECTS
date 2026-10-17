@echo off
title Restore Sub-Repositories: Switch to Individual Git Repositories
echo ========================================================
echo   Restoring Individual Sub-Repository Git Tracking
echo ========================================================
echo.

powershell -Command "$repos = @('AgriSage\AgriSage', 'Ai_Interview_Coach', 'amazon_ml_challenge', 'flutter-mobile_container', 'J_Code', 'ngo_volunteer_app'); foreach ($r in $repos) { if (Test-Path \"$r\.git_subrepo\") { Rename-Item -Path \"$r\.git_subrepo\" -NewName \".git\" -Force; Write-Output \"Restored $r sub-repository.\" } }"

echo.
echo Individual sub-repository mode is RESTORED.
pause
