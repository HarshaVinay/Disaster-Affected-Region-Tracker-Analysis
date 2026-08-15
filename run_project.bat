@echo off
echo [1/2] Running ETL...
python src\etl.py
if errorlevel 1 goto error
echo [2/2] Creating dashboard charts...
python src\dashboard.py
if errorlevel 1 goto error
echo.
echo Project completed. Check the output folder.
pause
exit /b 0
:error
echo.
echo Project failed. Check the error above.
pause
