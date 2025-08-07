# Full-Stack Appointment Booking Application

This project implements a minimal appointment booking application for a small clinic, organized as separate frontend and backend projects.

## Project Structure

```
appointment-booking-api/
├── src/
│   ├── models/user.py          # Database models (User, Slot, Booking)
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── slots.py           # Slot management endpoints
│   │   └── bookings.py        # Booking endpoints
│   ├── utils/auth.py          # JWT authentication middleware
│   ├── static/                # Built React frontend files
│   ├── database/app.db        # SQLite database
│   └── main.py               # Flask application entry point
├── requirements.txt
└── start.ps1                  # API management script

appointment-booking-frontend/
├── src/
│   ├── components/           # React components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── PatientDashboard.jsx
│   │   └── AdminDashboard.jsx
│   ├── App.jsx              # Main application with routing
│   ├── main.jsx             # React entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json           # Node.js dependencies
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
└── start.ps1              # Frontend management script
```

## Tech Stack

- **Backend**: Flask (Python) with SQLite database
- **Frontend**: React + Vite + Tailwind CSS
- **Authentication**: JWT tokens with role-based access control

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Option 1: Use the Main Script (Recommended)
```powershell
# Run the main management script
.\start.ps1
```

### Option 2: Manual Setup

#### 1. Install Dependencies
```powershell
# API dependencies
cd appointment-booking-api
pip install -r requirements.txt

# Frontend dependencies  
cd ../appointment-booking-frontend
npm install
```

#### 2a. Development Mode (Frontend + API separately)
```powershell
# Terminal 1 - Start API
cd appointment-booking-api\src
python main.py

# Terminal 2 - Start Frontend Dev Server
cd appointment-booking-frontend
npm run dev
```

#### 2b. Production Mode (Integrated)
```powershell
# Build frontend into API static directory
cd appointment-booking-frontend
npm run build

# Start Flask server (serves both API and built frontend)
cd ../appointment-booking-api/src
python main.py
```

## Access URLs

- **Development**: 
  - Frontend: http://localhost:5173
  - API: http://localhost:5000
- **Production**: http://localhost:5000 (integrated)

## Test Credentials

- **Patient**: patient@example.com / Passw0rd!
- **Admin**: admin@example.com / Passw0rd!

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `GET /api/slots` - Get available appointment slots
- `POST /api/book` - Book an appointment slot
- `GET /api/my-bookings` - Get patient's bookings (requires patient auth)
- `GET /api/all-bookings` - Get all bookings (requires admin auth)

## Features

-  User registration and authentication
-  Role-based access control (Patient/Admin)
-  JWT token-based authentication
-  Appointment slot booking with double-booking prevention
-  Patient dashboard to view and book appointments
-  Admin dashboard to view all bookings
-  Responsive design with Tailwind CSS
-  SQLite database with proper constraints
- CORS support for API access

## Development Workflow

### Frontend Development
```powershell
cd appointment-booking-frontend
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
```

### Backend Development
```powershell
cd appointment-booking-api
# Use start.ps1 script or run directly:
cd src
python main.py
```

## Build Configuration

The frontend is configured to build directly into the API's static directory:
- Build output: `appointment-booking-api/src/static/`
- This allows the Flask server to serve the built React app

## Scripts Available

### Main Directory
- `start.ps1` - Main management script with all options

### API Directory (`appointment-booking-api/`)
- `start.ps1` - API-specific management script

### Frontend Directory (`appointment-booking-frontend/`)
- `start.ps1` - Frontend-specific management script

## Architecture Notes

### Authentication Flow
1. User logs in via `/api/login`
2. JWT token stored in localStorage
3. Token sent in Authorization header for protected routes
4. Role-based access control (patient/admin)

### Concurrency Handling
- Database constraints prevent double-booking
- SQLite ACID properties ensure data consistency
- HTTP 409 Conflict returned for booking conflicts

### Error Handling
- Consistent JSON error format across all endpoints
- Proper HTTP status codes
- Client-side error display in UI

## Database

The application uses SQLite for simplicity. The database is automatically created at `database/app.db` when you first run the application.

### Default Admin User
An admin user is automatically created on first run:
- Email: admin@example.com
- Password: Passw0rd!

## Security Features

- bcrypt password hashing
- JWT token authentication
- Role-based access control
- Input validation and sanitization
- CORS configuration
- SQL injection prevention


## Test Credentials

- **Patient**: patient@example.com / Passw0rd!
- **Admin**: admin@example.com / Passw0rd!

