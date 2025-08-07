import sys
import os

# Add the API source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'appointment-booking-api', 'src'))

# Import the Flask app
from main import app

if __name__ == "__main__":
    app.run()
