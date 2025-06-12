from flask import Blueprint, request, jsonify, session, url_for
import datetime
from database import PostManager,AuditLogManager,UserManager
from .auth import login_required
from werkzeug.utils import secure_filename
import os

post_manager = PostManager()
audit_log_manager = AuditLogManager()
user_manager = UserManager()
posts_bp = Blueprint('posts', __name__)

UPLOAD_FOLDER = 'static/uploads_posts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_admin_action(user_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(user_id, action, resource_type, resource_id, details)

@posts_bp.route('/posts', methods=['POST'])
@login_required()
def create_post():
    """Create a new post for the authenticated user with an optional single image."""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Unauthorized: No active session'}), 401

    # Check if the request is form-data or JSON
    data = request.form.to_dict() if request.form else request.get_json() or {}
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and content cannot be empty'}), 400

    # Handle image: prioritize uploaded file, then image_url
    image_url = ''
    image_file_path = None
    if 'image' in request.files and request.files['image'].filename:
        file = request.files['image']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user_id}_{datetime.datetime.now().timestamp()}_{filename}"
            image_file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(image_file_path)
            image_url = url_for('static', filename=f'uploads_posts/{unique_filename}', _external=True)
        else:
            return jsonify({'error': 'Invalid or unsupported file type for image'}), 400
    elif 'image_url' in data and data['image_url']:
        if not data['image_url'].startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid image URL'}), 400
        image_url = data['image_url']

    try:
        post_id = post_manager.create_post(int(current_user_id), content, title, image_url)
        if post_id:
            new_post = post_manager.get_post_by_id(post_id)
            if new_post:
                post_data = {
                    'id': new_post[0],
                    'title': new_post[1],
                    'content': new_post[2],
                    'image': new_post[3],
                    'created_at': new_post[4].isoformat() + "Z" if isinstance(new_post[4], datetime.datetime) else str(new_post[4]),
                    'user_id': new_post[5],
                    'author': {
                        'first_name': new_post[6],
                        'last_name': new_post[7],
                        'photo': new_post[8]
                    }
                }
            else:
                post_data = {
                    'id': post_id,
                    'title': title,
                    'content': content,
                    'image': image_url,
                    'created_at': datetime.datetime.utcnow().isoformat() + "Z",
                    'user_id': int(current_user_id),
                    'author': None
                }
            log_admin_action(int(current_user_id), 'create_post', 'post', post_id, f"Created post with title: {title[:50]}")
            return jsonify({'message': 'Post created successfully', 'post': post_data}), 201
        else:
            # Clean up uploaded file if post creation fails
            if image_file_path and os.path.exists(image_file_path):
                os.remove(image_file_path)
            return jsonify({'error': 'Failed to create post'}), 500
    except Exception as e:
        # Clean up uploaded file on error
        if image_file_path and os.path.exists(image_file_path):
            os.remove(image_file_path)
        return jsonify({'error': f'Error creating post: {str(e)}'}), 500

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Retrieve a single post by its ID (authenticated)."""
    post = post_manager.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    post_data = {
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'image': post[3],
        'created_at': post[4].isoformat() + "Z" if isinstance(post[4], datetime.datetime) else str(post[4]),
        'user_id': post[5],
        'author': {
            'first_name': post[6],
            'last_name': post[7],
            'photo': post[8]
        }
    }
    return jsonify({'post': post_data}), 200

@posts_bp.route('/posts/<int:post_id>', methods=['GET', 'OPTIONS'])
def get_post_by_id(post_id):
    """Retrieve a single post by its ID (publicly accessible)."""
    post = post_manager.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    post_data = {
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'image': post[3],
        'created_at': post[4].isoformat() + "Z" if isinstance(post[4], datetime.datetime) else str(post[4]),
        'user_id': post[5],
        'author': {
            'first_name': post[6],
            'last_name': post[7],
            'photo': post[8]
        }
    }
    return jsonify({'post': post_data}), 200

@posts_bp.route('/posts/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """Retrieve posts for a user (publicly accessible)."""
    if not user_manager.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts, total = post_manager.get_posts_by_user(user_id, page, per_page)

    post_list = []
    for p in posts:
        post_dict = {
            'id': p[0],
            'title': p[1],
            'content': p[2],
            'image': p[3],
            'created_at': p[4].isoformat() + "Z" if isinstance(p[4], datetime.datetime) else str(p[4]),
            'user_id': p[5],
            'author': {
                'first_name': p[6],
                'last_name': p[7],
                'photo': p[8]
            }
        }
        post_list.append(post_dict)

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@posts_bp.route('/posts/admin_user_posts', methods=['GET', 'OPTIONS'])
def get_admin_user_posts():
    print("Fetching admin user posts------------------------------------")
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    admin_ids = user_manager.get_admin_ids()  # Get admin IDs from the database --> (1, 2, 3, ...)
    
    # Get posts for admins only
    posts, total = post_manager.get_posts_by_users(admin_ids, page, per_page)
    

    post_list = []
    for p in posts:
        post_dict = {
            'id': p[0],
            'title': p[1],
            'content': p[2],
            'image': p[3],
            'created_at': p[4].isoformat() + "Z" if isinstance(p[4], datetime.datetime) else str(p[4]),
            'user_id': p[5],
            'author': {
                'first_name': p[6],
                'last_name': p[7],
                'photo': p[8]
            }
        }
        post_list.append(post_dict)

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@posts_bp.route('/posts/users_posts', methods=['GET','OPTIONS'])
def get_all_posts_users():
    print("Fetching user posts------------------------------------")
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    user_ids = user_manager.get_users_ids()  # Get admin IDs from the database --> (1, 2, 3, ...)
    
    # Get posts for admins only
    posts, total = post_manager.get_posts_by_users(user_ids, page, per_page)
    

    post_list = []
    for p in posts:
        post_dict = {
            'id': p[0],
            'title': p[1],
            'content': p[2],
            'image': p[3],
            'created_at': p[4].isoformat() + "Z" if isinstance(p[4], datetime.datetime) else str(p[4]),
            'user_id': p[5],
            'author': {
                'first_name': p[6],
                'last_name': p[7],
                'photo': p[8]
            }
        }
        post_list.append(post_dict)

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@posts_bp.route('/posts', methods=['GET','OPTIONS'])
def get_all_posts():
    """Retrieve all posts (publicly accessible)."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts, total = post_manager.get_all_posts(page, per_page)

    post_list = []
    for p in posts:
        post_dict = {
            'id': p[0],
            'title': p[1],
            'content': p[2],
            'image': p[3],
            'created_at': p[4].isoformat() + "Z" if isinstance(p[4], datetime.datetime) else str(p[4]),
            'user_id': p[5],
            'author': {
                'first_name': p[6],
                'last_name': p[7],
                'photo': p[8]
            }
        }
        post_list.append(post_dict)

    return jsonify({
        'posts': post_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200
  
@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
@login_required()
def update_post(post_id):
    """Update an existing post with an optional single image."""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Unauthorized: No active session'}), 401

    post = post_manager.get_post_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Check if the user is the post owner or an admin
    if post[5] != int(current_user_id) and session.get('role') != 'admin':
        return jsonify({'error': 'Forbidden: You can only update your own posts'}), 403

    # Check if the request is form-data or JSON
    data = request.form.to_dict() if request.form else request.get_json() or {}
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and content cannot be empty'}), 400

    # Handle image: prioritize uploaded file, then image_url
    image_url = post[3]  # Retain existing image if no new image is provided
    image_file_path = None
    if 'image' in request.files and request.files['image'].filename:
        file = request.files['image']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user_id}_{datetime.datetime.now().timestamp()}_{filename}"
            image_file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(image_file_path)
            image_url = url_for('static', filename=f'uploads_posts/{unique_filename}', _external=True)
        else:
            return jsonify({'error': 'Invalid or unsupported file type for image'}), 400
    elif 'image_url' in data and data['image_url']:
        if not data['image_url'].startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid image URL'}), 400
        image_url = data['image_url']
    elif 'image_url' in data and not data['image_url']:
        image_url = None  # Allow clearing the image

    try:
        if post_manager.update_post(post_id, title, content, image_url):
            log_admin_action(int(current_user_id), 'update_post', 'post', post_id, f"Updated title: {title[:50]}, content: {content[:50]}")
            updated_post = post_manager.get_post_by_id(post_id)
            post_data = {
                'id': updated_post[0],
                'title': updated_post[1],
                'content': updated_post[2],
                'image': updated_post[3],
                'created_at': updated_post[4].isoformat() + "Z" if isinstance(updated_post[4], datetime.datetime) else str(updated_post[4]),
                'user_id': updated_post[5],
                'author': {
                    'first_name': updated_post[6],
                    'last_name': updated_post[7],
                    'photo': updated_post[8]
                }
            }
            return jsonify({'message': 'Post updated successfully', 'post': post_data}), 200
        else:
            # Clean up uploaded file if update fails
            if image_file_path and os.path.exists(image_file_path):
                os.remove(image_file_path)
            return jsonify({'error': 'Failed to update post'}), 500
    except Exception as e:
        # Clean up uploaded file on error
        if image_file_path and os.path.exists(image_file_path):
            os.remove(image_file_path)
        return jsonify({'error': f'Error updating post: {str(e)}'}), 500

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required()
def delete_post(post_id):
    """Delete a post by ID (admin only)."""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Unauthorized: No active session'}), 401

    if not post_manager.get_post_by_id(post_id):
        return jsonify({'error': 'Post not found'}), 404

    if post_manager.delete_post(post_id):
        log_admin_action(int(current_user_id), 'delete_post', 'post', post_id)
        return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete post'}), 500