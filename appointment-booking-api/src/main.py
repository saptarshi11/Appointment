import os
import sys

from flask import Flask, send_from_directory, request
try:
    from flask_cors import CORS
except ImportError:
    # Fallback if flask_cors is not available
    def CORS(app, **kwargs):
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response
        return app
from models.user import db, User
from routes.auth import auth_bp
from routes.slots import slots_bp
from routes.bookings import bookings_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins="*")

# Add request logging for debugging
@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.url}")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(slots_bp, url_prefix='/api')
app.register_blueprint(bookings_bp, url_prefix='/api')

# Health check route
@app.route('/api/health')
def health_check():
    return {"status": "OK", "message": "API is running"}

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def seed_admin_user():
    """Seed admin user if it doesn't exist"""
    admin_email = 'admin@example.com'
    admin_password = 'Passw0rd!'
    
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = User(
            name='Admin User',
            email=admin_email,
            role='admin'
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")

with app.app_context():
    db.create_all()
    seed_admin_user()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve React frontend files"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return {"error": "Static folder not configured"}, 404

    # If path is empty, serve index.html
    if path == "":
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return {"error": "Frontend not built. Run 'npm run build' in frontend directory."}, 404
    
    # Check if the requested file exists
    file_path = os.path.join(static_folder_path, path)
    if os.path.exists(file_path):
        return send_from_directory(static_folder_path, path)
    
    # For client-side routing, serve index.html
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return {"error": "Frontend not built. Run 'npm run build' in frontend directory."}, 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

