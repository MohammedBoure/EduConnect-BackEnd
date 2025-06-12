from flask import Blueprint, request, jsonify, session, url_for
from database import UserManager
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import re
import os

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

# Assuming user_manager is already defined elsewhere
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@auth_bp.route('/register', methods=['POST'])  # Update to '/api/register' if needed
def register():
    """Register a new user with optional photo upload or URL."""
    # Check if the request is JSON or form-data
    data = request.form.to_dict() if request.form else request.get_json() or {}
    required_fields = ['first_name', 'last_name', 'email', 'password', 'department', 'skills']
    
    # Validate required fields
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    password = data['password']
    
    # Validate email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password length
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Handle photo: prioritize uploaded file, then photo_url
    photo_url = ''
    file_path = None  # Track file path for cleanup
    if 'photo' in request.files and request.files['photo'].filename:
        file = request.files['photo']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Generate a unique filename to avoid conflicts
            unique_filename = f"{email.split('@')[0]}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            # Generate a URL for the uploaded file
            photo_url = url_for('static', filename=f'uploads/{unique_filename}', _external=True)
        else:
            return jsonify({'error': 'Invalid or unsupported file type'}), 400
    elif 'photo_url' in data and data['photo_url']:
        if not data['photo_url'].startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid photo URL'}), 400
        photo_url = data['photo_url']

    # Prepare user data
    user_data = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': email,
        'password': password,
        'department': data['department'],
        'skills': data['skills'].split(',') if isinstance(data['skills'], str) else data['skills'],
        'photo': photo_url,  # Store the final URL (uploaded or external)
        'role': 'user'  # Default role is 'user'
    }

    # Check if email is already registered
    if user_manager.get_user_by_email(email):
        # Clean up uploaded file if email is already registered
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': 'Email already registered'}), 400

    # Create user
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
                'photo': user['photo'],  # Return the stored URL
                'role': user['role']
            }
        }), 201
    
    # Clean up uploaded file if user creation fails
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
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