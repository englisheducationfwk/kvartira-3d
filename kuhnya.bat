@echo off
chcp 65001 >nul
rem 🏠 КУХНЯ 3D — игра-окно: сервер поднимается сам, консоль не мешает.
cd /d "%~dp0"
if not exist "index.html" python "_tools\build.py"
where pythonw >nul 2>nul
if errorlevel 1 (
    start "" python "play.py"
) else (
    start "" pythonw "play.py"
)
exit /b
