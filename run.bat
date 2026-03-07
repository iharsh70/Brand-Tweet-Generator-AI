@echo off
cd /d "%~dp0"
echo Starting Brand Tweet Generator...
echo.
echo App will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
C:\Python313\python.exe -m streamlit run app.py --server.headless true
pause
