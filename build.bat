@echo off
echo === NumaN Build Script ===
echo.

echo [1/3] Generating icon...
python src\numan\icon.py
echo.

echo [2/3] Building executable with PyInstaller...
python -m PyInstaller --clean numan.spec
echo.

echo [3/3] Build complete!
echo Output: dist\numan.exe
echo.
echo To create the installer, open installer\numan_setup.iss in Inno Setup and compile.
pause
