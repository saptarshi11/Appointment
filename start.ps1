# Appointment Booking System - PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Appointment Booking System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Yellow
    Write-Host "1. Setup - Install all dependencies" -ForegroundColor White
    Write-Host "2. Development - Start frontend dev server" -ForegroundColor White
    Write-Host "3. Development - Start API server" -ForegroundColor White
    Write-Host "4. Production - Build and start full application" -ForegroundColor White
    Write-Host "5. Go to API directory" -ForegroundColor White
    Write-Host "6. Go to Frontend directory" -ForegroundColor White
    Write-Host "7. Exit" -ForegroundColor White
    Write-Host ""
}

function Install-AllDependencies {
    Write-Host "Installing all dependencies..." -ForegroundColor Green
    
    Write-Host "Installing API dependencies..." -ForegroundColor Yellow
    Set-Location appointment-booking-api
    pip install -r requirements.txt
    Set-Location ..
    
    Write-Host "Installing Frontend dependencies..." -ForegroundColor Yellow
    Set-Location appointment-booking-frontend
    npm install
    Set-Location ..
    
    Write-Host "All dependencies installed successfully!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function Start-FrontendDev {
    Write-Host "Starting frontend development server..." -ForegroundColor Green
    Write-Host "Make sure API is running on http://localhost:5000" -ForegroundColor Yellow
    Write-Host "Frontend will be available at http://localhost:5173" -ForegroundColor Yellow
    Set-Location appointment-booking-frontend
    npm run dev
}

function Start-APIServer {
    Write-Host "Starting Flask API server..." -ForegroundColor Green
    Write-Host "API will be available at http://localhost:5000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Test Credentials:" -ForegroundColor Cyan
    Write-Host "Patient: patient@example.com / Passw0rd!" -ForegroundColor White
    Write-Host "Admin: admin@example.com / Passw0rd!" -ForegroundColor White
    Write-Host ""
    Set-Location appointment-booking-api\src
    python main.py
}

function Start-FullApplication {
    Write-Host "Building frontend and starting full application..." -ForegroundColor Green
    
    Write-Host "Building frontend..." -ForegroundColor Yellow
    Set-Location appointment-booking-frontend
    npm run build
    Set-Location ..
    
    Write-Host "Starting Flask application with built frontend..." -ForegroundColor Yellow
    Write-Host "Application will be available at http://localhost:5000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Test Credentials:" -ForegroundColor Cyan
    Write-Host "Patient: patient@example.com / Passw0rd!" -ForegroundColor White
    Write-Host "Admin: admin@example.com / Passw0rd!" -ForegroundColor White
    Write-Host ""
    Set-Location appointment-booking-api\src
    python main.py
}

function Open-APIDirectory {
    Write-Host "Opening API directory..." -ForegroundColor Green
    Set-Location appointment-booking-api
    Write-Host "You are now in the API directory. Run './start.ps1' for API-specific options." -ForegroundColor Yellow
    powershell
}

function Open-FrontendDirectory {
    Write-Host "Opening Frontend directory..." -ForegroundColor Green
    Set-Location appointment-booking-frontend
    Write-Host "You are now in the Frontend directory. Run './start.ps1' for frontend-specific options." -ForegroundColor Yellow
    powershell
}

# Main loop
do {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Appointment Booking System" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Menu
    $choice = Read-Host "Enter your choice (1-7)"
    
    switch ($choice) {
        "1" { Install-AllDependencies }
        "2" { Start-FrontendDev }
        "3" { Start-APIServer }
        "4" { Start-FullApplication }
        "5" { Open-APIDirectory }
        "6" { Open-FrontendDirectory }
        "7" { 
            Write-Host "Goodbye!" -ForegroundColor Green
            exit 
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Read-Host "Press Enter to continue"
        }
    }
} while ($true)
