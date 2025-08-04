@echo off
setlocal enabledelayedexpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="setup" goto setup
if "%1"=="run-backend" goto run-backend
if "%1"=="run-frontend" goto run-frontend
if "%1"=="run-all" goto run-all
if "%1"=="notebooks" goto notebooks
if "%1"=="test" goto test
if "%1"=="clean" goto clean
if "%1"=="run-analysis" goto run-analysis
if "%1"=="quick-start" goto quick-start
goto help

:help
echo Brent Oil Price Analysis - Available Commands:
echo.
echo Setup Commands:
echo   install     - Install all dependencies
echo   setup       - Setup the project (install + data preparation)
echo.
echo Run Commands:
echo   run-backend - Start the Flask backend server
echo   run-frontend- Start the React frontend development server
echo   run-all     - Start both backend and frontend
echo.
echo Analysis Commands:
echo   notebooks   - Run Jupyter notebooks for analysis
echo   test        - Run tests
echo   run-analysis- Run complete analysis pipeline
echo.
echo Utility Commands:
echo   clean       - Clean generated files
echo   help        - Show this help message
echo   quick-start - Setup and run everything
echo.
echo Usage: run.bat [command]
goto end

:install
echo Installing Python dependencies...
pip install -r requirements.txt
echo Installing backend dependencies...
cd src\backend && pip install -r requirements.txt && cd ..\..
echo Installing frontend dependencies...
cd src\frontend\oil-price-dashboard && npm install && cd ..\..\..
echo Installation complete!
goto end

:setup
call :install
echo Setting up the project...
echo Creating output directories...
if not exist "data\outputs" mkdir data\outputs
if not exist "data\processed" mkdir data\processed
echo Setup complete! Run 'run.bat run-all' to start the application.
goto end

:run-backend
echo Starting Flask backend server...
cd src\backend && python app.py
goto end

:run-frontend
echo Starting React frontend development server...
cd src\frontend\oil-price-dashboard && npm start
goto end

:run-all
echo Starting both backend and frontend...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Starting backend in background...
start "Backend Server" cmd /k "cd src\backend && python app.py"
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul
echo Starting frontend...
cd src\frontend\oil-price-dashboard && npm start
goto end

:notebooks
echo Running Jupyter notebooks...
jupyter notebook notebooks\
goto end

:test
echo Running tests...
python -m pytest src\analysis\tests\ -v
python -m pytest src\backend\tests\ -v
goto end

:clean
echo Cleaning generated files...
if exist "data\outputs" rmdir /s /q data\outputs
if exist "data\processed" rmdir /s /q data\processed
if exist "src\frontend\oil-price-dashboard\build" rmdir /s /q src\frontend\oil-price-dashboard\build
if exist "src\frontend\oil-price-dashboard\node_modules" rmdir /s /q src\frontend\oil-price-dashboard\node_modules
for /r . %%f in (*.pyc) do del "%%f"
for /d /r . %%d in (__pycache__) do rmdir /s /q "%%d"
echo Cleanup complete!
goto end

:run-analysis
echo Running complete analysis pipeline...
python run_analysis.py
goto end

:quick-start
call :setup
echo Quick start guide:
echo 1. Backend is starting at http://localhost:5000
echo 2. Frontend is starting at http://localhost:3000
echo 3. Wait for both servers to start, then open http://localhost:3000
echo.
echo Starting servers...
call :run-all
goto end

:end 