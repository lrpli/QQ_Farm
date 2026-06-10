@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   QQFarmBot EXE Build Script
echo ========================================
echo.

:: Clean old build
echo [1/3] Cleaning old build...
rmdir /s /q build 2>nul
rmdir /s /q dist\QQFarmBot 2>nul
del /f /q dist\QQFarmBot.exe 2>nul

:: Build
echo [2/3] Building QQFarmBot...
python -m PyInstaller build.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

:: Verify
echo.
echo [3/3] Verifying...
if exist "dist\QQFarmBot.exe" (
    for %%A in (dist\QQFarmBot.exe) do echo EXE: %%~zA bytes
    echo [OK] Build complete! Output: dist\QQFarmBot.exe
    echo.
    pause
    exit /b 0
)

if exist "dist\QQFarmBot\QQFarmBot.exe" (
    for %%A in (dist\QQFarmBot\QQFarmBot.exe) do echo EXE: %%~zA bytes
    if not exist "dist\QQFarmBot\_internal\templates" (
        echo [WARNING] templates directory missing!
    )
    echo [OK] Build complete! Output: dist\QQFarmBot\
    echo.
    pause
    exit /b 0
)

echo [ERROR] QQFarmBot.exe not found!
echo.
pause
