from flask import Blueprint, jsonify, request
from models.user import User, db
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({
                'error': {
                    'code': 'MISSING_FIELDS',
                    'message': 'Name, email, and password are required'
                }
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'error': {
                    'code': 'EMAIL_EXISTS',
                    'message': 'User with this email already exists'
                }
            }), 409
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            role='patient'  # Default role
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': {
                'code': 'REGISTRATION_FAILED',
                'message': str(e)
            }
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'error': {
                    'code': 'MISSING_CREDENTIALS',
                    'message': 'Email and password are required'
                }
            }), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        # Check credentials
        if not user or not user.check_password(data['password']):
            return jsonify({
                'error': {
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'Invalid email or password'
                }
            }), 401
        
        # Generate token
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'token': token,
            'role': user.role,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'LOGIN_FAILED',
                'message': str(e)
            }
        }), 500

