param(
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Brent Oil Price Analysis - Available Commands:" -ForegroundColor Green
    Write-Host ""
    Write-Host "Setup Commands:" -ForegroundColor Yellow
    Write-Host "  install     - Install all dependencies"
    Write-Host "  setup       - Setup the project (install + data preparation)"
    Write-Host ""
    Write-Host "Run Commands:" -ForegroundColor Yellow
    Write-Host "  run-backend - Start the Flask backend server"
    Write-Host "  run-frontend- Start the React frontend development server"
    Write-Host "  run-all     - Start both backend and frontend"
    Write-Host ""
    Write-Host "Analysis Commands:" -ForegroundColor Yellow
    Write-Host "  notebooks   - Run Jupyter notebooks for analysis"
    Write-Host "  test        - Run tests"
    Write-Host "  run-analysis- Run complete analysis pipeline"
    Write-Host ""
    Write-Host "Utility Commands:" -ForegroundColor Yellow
    Write-Host "  clean       - Clean generated files"
    Write-Host "  help        - Show this help message"
    Write-Host "  quick-start - Setup and run everything"
    Write-Host ""
    Write-Host "Usage: .\run.ps1 [command]" -ForegroundColor Cyan
}

function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
    
    Write-Host "Installing backend dependencies..." -ForegroundColor Green
    Set-Location src\backend
    pip install -r requirements.txt
    Set-Location ..\..
    
    Write-Host "Installing frontend dependencies..." -ForegroundColor Green
    Set-Location src\frontend\oil-price-dashboard
    npm install
    Set-Location ..\..\..
    
    Write-Host "Installation complete!" -ForegroundColor Green
}

function Setup-Project {
    Install-Dependencies
    Write-Host "Setting up the project..." -ForegroundColor Green
    Write-Host "Creating output directories..." -ForegroundColor Green
    
    if (!(Test-Path "data\outputs")) { New-Item -ItemType Directory -Path "data\outputs" -Force }
    if (!(Test-Path "data\processed")) { New-Item -ItemType Directory -Path "data\processed" -Force }
    
    Write-Host "Setup complete! Run '.\run.ps1 run-all' to start the application." -ForegroundColor Green
}

function Start-Backend {
    Write-Host "Starting Flask backend server..." -ForegroundColor Green
    Set-Location src\backend
    python app.py
}

function Start-Frontend {
    Write-Host "Starting React frontend development server..." -ForegroundColor Green
    Set-Location src\frontend\oil-price-dashboard
    npm start
}

function Start-All {
    Write-Host "Starting both backend and frontend..." -ForegroundColor Green
    Write-Host "Backend will be available at: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Starting backend in background..." -ForegroundColor Green
    
    Start-Process powershell -ArgumentList "-Command", "Set-Location src\backend; python app.py" -WindowStyle Normal
    
    Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    Write-Host "Starting frontend..." -ForegroundColor Green
    Set-Location src\frontend\oil-price-dashboard
    npm start
}

function Start-Notebooks {
    Write-Host "Running Jupyter notebooks..." -ForegroundColor Green
    jupyter notebook notebooks\
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Green
    python -m pytest src\analysis\tests\ -v
    python -m pytest src\backend\tests\ -v
}

function Clean-Project {
    Write-Host "Cleaning generated files..." -ForegroundColor Green
    if (Test-Path "data\outputs") { Remove-Item "data\outputs" -Recurse -Force }
    if (Test-Path "data\processed") { Remove-Item "data\processed" -Recurse -Force }
    if (Test-Path "src\frontend\oil-price-dashboard\build") { Remove-Item "src\frontend\oil-price-dashboard\build" -Recurse -Force }
    if (Test-Path "src\frontend\oil-price-dashboard\node_modules") { Remove-Item "src\frontend\oil-price-dashboard\node_modules" -Recurse -Force }
    
    Get-ChildItem -Recurse -Include "*.pyc" | Remove-Item -Force
    Get-ChildItem -Recurse -Include "__pycache__" -Directory | Remove-Item -Recurse -Force
    
    Write-Host "Cleanup complete!" -ForegroundColor Green
}

function Run-Analysis {
    Write-Host "Running complete analysis pipeline..." -ForegroundColor Green
    python run_analysis.py
}

function Quick-Start {
    Setup-Project
    Write-Host "Quick start guide:" -ForegroundColor Green
    Write-Host "1. Backend is starting at http://localhost:5000" -ForegroundColor Cyan
    Write-Host "2. Frontend is starting at http://localhost:3000" -ForegroundColor Cyan
    Write-Host "3. Wait for both servers to start, then open http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Starting servers..." -ForegroundColor Green
    Start-All
}

# Main execution
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "setup" { Setup-Project }
    "run-backend" { Start-Backend }
    "run-frontend" { Start-Frontend }
    "run-all" { Start-All }
    "notebooks" { Start-Notebooks }
    "test" { Run-Tests }
    "clean" { Clean-Project }
    "run-analysis" { Run-Analysis }
    "quick-start" { Quick-Start }
    default { Show-Help }
} 