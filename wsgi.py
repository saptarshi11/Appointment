import sys
import os

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))
api_src_path = os.path.join(project_root, 'appointment-booking-api', 'src')

# Add the API source directory to Python path
if api_src_path not in sys.path:
    sys.path.insert(0, api_src_path)

# Change to the API directory to ensure relative paths work
os.chdir(api_src_path)

# Import the Flask app
try:
    from main import app
    print(f"Successfully imported Flask app from {api_src_path}")
except ImportError as e:
    print(f"Error importing main: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
