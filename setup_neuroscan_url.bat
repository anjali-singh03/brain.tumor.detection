@echo off
title Setup NeuroScan Local URL
echo ====================================================================
echo  NeuroScan PACS - Configuring Local Domain: http://neuroscan.local:8501
echo ====================================================================
echo.

:: Check for Administrator permissions
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [PROMPT] Requesting Administrator access to update your Windows hosts file...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: Check if already mapped
findstr /I "neuroscan.local" "%SystemRoot%\System32\drivers\etc\hosts" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 'neuroscan.local' is already mapped in your hosts file.
) else (
    echo. >> "%SystemRoot%\System32\drivers\etc\hosts"
    echo # NeuroScan PACS Workstation >> "%SystemRoot%\System32\drivers\etc\hosts"
    echo 127.0.0.1    neuroscan.local neuroscan >> "%SystemRoot%\System32\drivers\etc\hosts"
    echo [SUCCESS] Successfully added 'neuroscan.local' and 'neuroscan' to Windows hosts file!
)

:: Flush DNS cache to apply immediately
ipconfig /flushdns >nul

echo.
echo ====================================================================
echo  SETUP COMPLETE! You can now use either of these URLs in any browser:
echo.
echo    http://neuroscan.local:8501
echo    http://neuroscan:8501
echo ====================================================================
echo.
pause
