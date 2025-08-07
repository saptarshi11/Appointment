#!/bin/bash

# Navigate to the API directory
cd appointment-booking-api/src

# Start the Flask application with gunicorn
gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000}
