---
description: Compiles the PaperInk Python application into a standalone Windows executable (.exe) using PyInstaller.
---

This workflow automates the process of generating assets and compiling the PaperInk application for distribution.

### Prerequisites
- Python 3.12 (x86/x64)
- dependencies installed (`pip install -r requirements.txt`)

### Steps

1. **Clean previous builds**
// turbo
```powershell
if (Test-Path "python_app/build") { Remove-Item "python_app/build" -Recurse -Force }
if (Test-Path "python_app/dist") { Remove-Item "python_app/dist" -Recurse -Force }
```

2. **Generate latest icons and MSIX assets**
// turbo
```powershell
python python_app/build_msix_assets.py
```

3. **Compile standalone executable**
// turbo
```powershell
cd python_app
pyinstaller --onefile --windowed `
    --icon="assets/icon.ico" `
    --add-data "assets;assets" `
    --name "PaperInk" `
    main.py
```

4. **Verify output**
Check if the executable exists in `python_app/dist/PaperInk.exe`.

---
*Note: For official Microsoft Store releases, use the master build script via `.\compile_and_master.ps1` instead.*
