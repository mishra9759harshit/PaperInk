@echo off

rem ------------------------------------------------------------
rem PaperInk PyInstaller Compilation Script
rem ------------------------------------------------------------

rem Path to custom Python executable (provided by user)
set "PYTHON_EXE=C:\Users\mishr\Downloads\python-3.12.9.exe"

rem Ensure we are in the project root (python_app folder)
cd /d "%~dp0"

rem ------------------------------------------------------------
rem Step 1: Install required dependencies (optional if already installed)
rem ------------------------------------------------------------
%PYTHON_EXE% -m pip install -r requirements.txt

rem ------------------------------------------------------------
rem Step 2: Clean previous build artifacts
rem ------------------------------------------------------------
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"

rem ------------------------------------------------------------
rem Step 3: Generate latest icons and MSIX assets
rem ------------------------------------------------------------
%PYTHON_EXE% build_msix_assets.py

rem ------------------------------------------------------------
rem Step 4: Compile the standalone executable with media bundled
rem ------------------------------------------------------------
%PYTHON_EXE% -m PyInstaller --onefile --windowed ^
    --icon="assets\icon.ico" ^
    --add-data "assets;assets" ^
    --name "PaperInk" ^
    main.py

rem ------------------------------------------------------------
rem Step 5: Verify output
rem ------------------------------------------------------------
if exist "dist\PaperInk.exe" (
    echo Compilation successful! Executable located at "dist\PaperInk.exe"
) else (
    echo Compilation failed. Check the console output for errors.
)

pause
