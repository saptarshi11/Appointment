#!/usr/bin/env python3
import os
import sys

# Change to the correct directory
project_root = os.path.dirname(os.path.abspath(__file__))
api_src_path = os.path.join(project_root, 'appointment-booking-api', 'src')

# Add to Python path
sys.path.insert(0, api_src_path)

# Change working directory
os.chdir(api_src_path)

# Import and run the app
from main import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
