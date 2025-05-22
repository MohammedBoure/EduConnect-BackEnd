from flask import Blueprint, request, jsonify, session
from database import UserManager
from werkzeug.security import check_password_hash
from functools import wraps
import re

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # السماح بمرور طلب OPTIONS بدون التحقق من الجلسة
            if request.method == 'OPTIONS':
                return '', 200

            if 'user_id' not in session:
                return jsonify({'error': 'Unauthorized: No active session'}), 401

            user = user_manager.get_user_by_id(session['user_id'])
            if not user:
                session.clear()
                return jsonify({'error': 'Unauthorized: User not found'}), 401

            if session.get('role') != user['role']:
                session.clear()
                return jsonify({'error': 'Session invalid due to role change, please log in again'}), 401

            if role and user['role'] != role:
                return jsonify({'error': f'Forbidden: Requires {role} role'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'email', 'password', 'department', 'skills']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    password = data['password']
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'error': 'Invalid email format'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    user_data = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': email,
        'password': password,
        'department': data['department'],
        'skills': data['skills'] if isinstance(data['skills'], list) else data['skills'].split(','),
        'photo': data.get('photo', ''),
        'role': 'user'  # Default role is 'user'
    }

    if user_manager.get_user_by_email(email):
        return jsonify({'error': 'Email already registered'}), 400

    user_id = user_manager.create_user(**user_data)
    if user_id:
        user = user_manager.get_user_by_id(user_id)
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'department': user['department'],
                'photo': user['photo'],
                'role': user['role']
            }
        }), 201
    return jsonify({'error': 'Failed to register user'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = user_manager.get_user_by_email(data['email'])
    if user and check_password_hash(user['password'], data['password']):
        session['user_id'] = str(user['id'])  # Store user ID in session
        session['role'] = user['role']  # Store user role in session
        session.permanent = True  # Persist session based on PERMANENT_SESSION_LIFETIME
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user_id from session
    session.pop('role', None)  # Remove role from session
    return jsonify({'message': 'Logged out successfully'}), 200