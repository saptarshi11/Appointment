# Full-Stack Appointment Booking Application

This project implements a minimal appointment booking application for a small clinic, as a full-stack take-home assignment.

## Tech Stack Choices

- **Backend**: Flask (Python) - Chosen for its lightweight nature and rapid development capabilities, suitable for a small API with built-in development server.
- **Frontend**: ReactJS - A popular JavaScript library for building user interfaces, offering a component-based structure and efficient rendering with excellent developer experience.
- **Database**: SQLite - Selected for its simplicity and file-based nature, making it easy to set up and manage for a demo application without external database dependencies.
- **Authentication**: JWT (JSON Web Tokens) - Provides a secure and stateless way to handle user authentication and authorization with role-based access control.

**Trade-offs**: SQLite is perfect for development but would need to be replaced with PostgreSQL for production. Flask's development server is used for simplicity but would require a production WSGI server like Gunicorn for deployment.

## How to Run Locally

### Backend (Flask API)
```bash
cd appointment-booking-api
source venv/bin/activate
python src/main.py
```
The API will be available at http://localhost:5000

### Frontend (React - Development Mode)
```bash
cd appointment-booking-frontend
pnpm run dev --host
```
The frontend will be available at http://localhost:5173

### Full-Stack (Production Build)
The React frontend has been built and integrated into the Flask application:
```bash
cd appointment-booking-api
source venv/bin/activate
python src/main.py
```
Access the complete application at http://localhost:5000

## Environment Variables

No additional environment variables are required for local development. The application uses:
- `SECRET_KEY`: Set to a default value in the Flask app (should be changed for production)
- Database: SQLite file stored in `src/database/app.db`

## Test Credentials

- **Patient**: patient@example.com / Passw0rd!
- **Admin**: admin@example.com / Passw0rd!

## Architecture Notes

### Folder Structure Rationale

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
└── requirements.txt

appointment-booking-frontend/
├── src/
│   ├── components/           # React components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── PatientDashboard.jsx
│   │   └── AdminDashboard.jsx
│   └── App.jsx              # Main application with routing
└── dist/                    # Production build output
```

### Authentication and Role-Based Access Control (RBAC) Approach

- Users register and log in using email and password with bcrypt hashing
- Upon successful login, a JWT is issued containing the user's ID and role (patient or admin)
- JWT tokens are stored in localStorage and sent with subsequent requests via Authorization header
- Backend middleware (`@token_required` decorator) verifies JWT and enforces role-based access
- Patients can only access their own bookings, admins can view all bookings

### Concurrency/Atomicity for Booking

- **Database Constraint**: Unique constraint on `bookings.slot_id` prevents double-booking at the database level
- **Application Logic**: Before creating a booking, the system checks if the slot is already booked
- **Error Handling**: If a slot is already taken, returns HTTP 409 Conflict with clear error message
- **Race Condition Protection**: SQLite's ACID properties and the unique constraint ensure atomicity

### Error Handling Strategy

- **Consistent Error Format**: All API errors return JSON in format `{ "error": { "code": "ERROR_CODE", "message": "Description" } }`
- **HTTP Status Codes**: Proper use of 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict)
- **Frontend Error Display**: Errors are displayed in-UI using alert components
- **Input Validation**: Server-side validation for all required fields and data types
- **Database Error Handling**: Graceful handling of constraint violations and rollback on errors

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `GET /api/slots` - Get available appointment slots
- `POST /api/book` - Book an appointment slot
- `GET /api/my-bookings` - Get patient's bookings (requires patient auth)
- `GET /api/all-bookings` - Get all bookings (requires admin auth)

## Quick Verification Script

Test the API endpoints with these curl commands:

```bash
# 1. Register a new patient
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "Passw0rd!"}'

# 2. Login as patient
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "patient@example.com", "password": "Passw0rd!"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

# 3. Get available slots
curl -X GET http://localhost:5000/api/slots

# 4. Book a slot (replace 1 with an available slot ID)
curl -X POST http://localhost:5000/api/book \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"slotId": 1}'

# 5. Get patient bookings
curl -X GET http://localhost:5000/api/my-bookings \
  -H "Authorization: Bearer $TOKEN"

# 6. Login as admin and get all bookings
ADMIN_TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "Passw0rd!"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")

curl -X GET http://localhost:5000/api/all-bookings \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Features Implemented

✅ **Core User Stories**
- Patient registration and login
- View available slots for next 7 days
- Book appointment slots with double-booking prevention
- View patient's own bookings
- Admin login and view all bookings

✅ **Technical Requirements**
- REST API with proper HTTP status codes and JSON responses
- JWT authentication with role-based access control
- SQLite database with proper schema and constraints
- Input validation and error handling
- CORS support for frontend-backend communication

✅ **Frontend Features**
- React application with routing
- Login/Register forms with validation
- Patient dashboard with slot booking
- Admin dashboard with booking overview
- Responsive design with Tailwind CSS
- Authentication state persistence
- Error handling and loading states

## Known Limitations and Future Improvements

**Current Limitations:**
1. **Database**: Using SQLite which is not suitable for production concurrent access
2. **Authentication**: JWT tokens don't have refresh mechanism
3. **Time Zones**: All times are in server local time, not user-specific
4. **Slot Generation**: Slots are generated on-demand, could be pre-populated
5. **No Email Notifications**: Booking confirmations are not sent via email

**With 2 More Hours, I Would Add:**
1. **Database Migration**: Switch to PostgreSQL with proper connection pooling
2. **Enhanced Security**: Add rate limiting, password strength requirements, and JWT refresh tokens
3. **Email Integration**: Send booking confirmation emails using SendGrid or similar
4. **Time Zone Support**: Allow users to set their timezone preferences
5. **Booking Management**: Allow patients to cancel bookings and admins to manage slots
6. **Testing**: Add comprehensive unit tests and integration tests
7. **Docker**: Containerize the application for easier deployment
8. **Logging**: Add structured logging for better monitoring and debugging

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Role-based access control
- Input validation and sanitization
- CORS configuration
- SQL injection prevention through ORM
- No sensitive data in client-side storage (only JWT token)

## Deployment Notes

The application is ready for deployment with the frontend built and integrated into the Flask static directory. For production deployment:

1. Use a production WSGI server (Gunicorn)
2. Set up a proper database (PostgreSQL)
3. Configure environment variables for secrets
4. Set up HTTPS with SSL certificates
5. Configure proper CORS origins
6. Add monitoring and logging


