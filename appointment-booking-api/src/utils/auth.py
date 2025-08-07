from functools import wraps
from flask import request, jsonify
import jwt
import os
from models.user import User

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'error': {
                        'code': 'INVALID_TOKEN_FORMAT',
                        'message': 'Token format should be: Bearer <token>'
                    }
                }), 401
        
        if not token:
            return jsonify({
                'error': {
                    'code': 'TOKEN_MISSING',
                    'message': 'Authentication token is required'
                }
            }), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({
                    'error': {
                        'code': 'USER_NOT_FOUND',
                        'message': 'User not found'
                    }
                }), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': {
                    'code': 'TOKEN_EXPIRED',
                    'message': 'Token has expired'
                }
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid token'
                }
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated