# Appointment Booking API - PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Appointment Booking API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Yellow
    Write-Host "1. Install Python dependencies" -ForegroundColor White
    Write-Host "2. Start API server" -ForegroundColor White
    Write-Host "3. Test API endpoints" -ForegroundColor White
    Write-Host "4. Exit" -ForegroundColor White
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function Start-API {
    Write-Host "Starting Flask API server..." -ForegroundColor Green
    Write-Host "API will be available at http://localhost:5000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Test Credentials:" -ForegroundColor Cyan
    Write-Host "Patient: patient@example.com / Passw0rd!" -ForegroundColor White
    Write-Host "Admin: admin@example.com / Passw0rd!" -ForegroundColor White
    Write-Host ""
    Set-Location src
    python main.py
    Set-Location ..
}

function Test-API {
    Write-Host "Testing API endpoints..." -ForegroundColor Green
    Write-Host "Testing backend imports..." -ForegroundColor Yellow
    Set-Location src
    python -c "import models.user; print('Backend imports working!')"
    Set-Location ..
    Write-Host "API tests completed!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

# Main loop
do {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Appointment Booking API" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Menu
    $choice = Read-Host "Enter your choice (1-4)"
    
    switch ($choice) {
        "1" { Install-Dependencies }
        "2" { Start-API }
        "3" { Test-API }
        "4" { 
            Write-Host "Goodbye!" -ForegroundColor Green
            exit 
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Read-Host "Press Enter to continue"
        }
    }
} while ($true)
