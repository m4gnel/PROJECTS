@echo off
title AgriSage Emulator Launcher
echo ========================================================
echo   Launching AgriSage Android Mobile App in Emulator
echo ========================================================
echo.
echo [1/3] Starting Android Emulator window on your screen...

cd /d "C:\Users\MAGNEL\AppData\Local\Android\Sdk\emulator"
start "" "emulator.exe" -avd Medium_Phone_API_37.0 -gpu host

echo [2/3] Waiting for Android OS to finish booting...
cd /d "C:\Users\MAGNEL\AppData\Local\Android\Sdk\platform-tools"
adb.exe wait-for-device

:wait_boot
timeout /t 2 /nobreak >nul
for /f "tokens=*" %%a in ('adb.exe shell getprop sys.boot_completed 2^>nul') do set BOOT=%%a
if not "%BOOT%"=="1" goto wait_boot

echo [3/3] Android is ready! Unlocking screen and launching AgriSage...
timeout /t 1 /nobreak >nul
adb.exe shell input keyevent 82
timeout /t 1 /nobreak >nul
adb.exe shell am start -n com.agrisage.app/.MainActivity

echo.
echo ========================================================
echo   AgriSage App is now running on your screen!
echo ========================================================
timeout /t 5 /nobreak >nul
