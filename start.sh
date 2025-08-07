#!/bin/bash

# Navigate to the API directory
cd appointment-booking-api/src

# Start the Flask application with gunicorn
gunicorn wsgi:app --host 0.0.0.0 --port ${PORT:-5000}
