# Appointment Booking Frontend - PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Appointment Booking Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Yellow
    Write-Host "1. Install Node.js dependencies" -ForegroundColor White
    Write-Host "2. Start development server" -ForegroundColor White
    Write-Host "3. Build for production" -ForegroundColor White
    Write-Host "4. Preview production build" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Green
    npm install
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function Start-Development {
    Write-Host "Starting frontend development server..." -ForegroundColor Green
    Write-Host "Make sure API is running on http://localhost:5000" -ForegroundColor Yellow
    Write-Host "Frontend will be available at http://localhost:5173" -ForegroundColor Yellow
    npm run dev
}

function Build-Production {
    Write-Host "Building frontend for production..." -ForegroundColor Green
    Write-Host "Output will be built to ../appointment-booking-api/src/static" -ForegroundColor Yellow
    npm run build
    Write-Host "Frontend built successfully!" -ForegroundColor Green
    Write-Host "You can now start the API server to serve the full application" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
}

function Preview-Production {
    Write-Host "Starting production preview server..." -ForegroundColor Green
    Write-Host "Make sure you've built the project first (option 3)" -ForegroundColor Yellow
    npm run preview
}

# Main loop
do {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Appointment Booking Frontend" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Menu
    $choice = Read-Host "Enter your choice (1-5)"
    
    switch ($choice) {
        "1" { Install-Dependencies }
        "2" { Start-Development }
        "3" { Build-Production }
        "4" { Preview-Production }
        "5" { 
            Write-Host "Goodbye!" -ForegroundColor Green
            exit 
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Read-Host "Press Enter to continue"
        }
    }
} while ($true)
