@echo off
cd /d "%~dp0"

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pillow pyinstaller

echo.
echo Building EXE...
python -m PyInstaller --onefile --console --name MetadataCleaner metadata_cleaner_drop_tool.py

echo.
if exist "dist\MetadataCleaner.exe" (
  echo SUCCESS
  echo Your EXE is here:
  echo %cd%\dist\MetadataCleaner.exe
) else (
  echo FAILED
  echo The EXE was not created. Read the error messages above.
)

echo.
pause