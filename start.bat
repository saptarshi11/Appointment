@echo off
echo ========================================
echo   Appointment Booking System
echo ========================================
echo.

:menu
echo Choose an option:
echo 1. Install dependencies
echo 2. Build frontend for production
echo 3. Start development (frontend only)
echo 4. Start backend (API only)
echo 5. Start full application (production)
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto build
if "%choice%"=="3" goto dev
if "%choice%"=="4" goto backend
if "%choice%"=="5" goto full
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:install
echo Installing dependencies...
echo Installing Python dependencies...
pip install -r requirements.txt
echo Installing Node.js dependencies...
npm install
echo Dependencies installed successfully!
pause
goto menu

:build
echo Building frontend for production...
npm run build
echo Frontend built successfully!
pause
goto menu

:dev
echo Starting frontend development server...
echo Backend should be running on http://localhost:5000
npm run dev
pause
goto menu

:backend
echo Starting Flask backend...
python main.py
pause
goto menu

:full
echo Building frontend and starting full application...
npm run build
echo Starting Flask application with built frontend...
python main.py
pause
goto menu

:exit
echo Goodbye!
exit
