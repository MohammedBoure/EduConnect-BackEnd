from flask import Blueprint, request, jsonify, session
from .auth import login_required
from database import UserManager,AuditLogManager

profile_bp = Blueprint('profile', __name__)

user_manager = UserManager()
audit_log_manager = AuditLogManager()

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Retrieve details of a specific user by ID."""
    user = user_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    skills = user_manager.search_users(skill='', exclude_user_id=None, page=1, per_page=1)[0]
    skills_list = [skill.strip() for skill in skills[0]['skills'].split(',') if skill.strip()] if skills[0]['skills'] else []
    
    return jsonify({
        'id': user['id'],
        'last_name': user['last_name'],
        'first_name': user['first_name'],
        'email': user['email'],
        'department': user['department'],
        'skills': skills_list,
        'photo': user['photo'],
        'role': user['role']
    }), 200

# Function to serialize user data
def serialize_user(user):
    """Serialize user data for API response."""
    # Accessing skills using indexing since it's a sqlite3.Row object
    skills = user['skills'] if 'skills' in user else []
    if isinstance(skills, str):
        skills = [skill.strip() for skill in skills.split(',') if skill.strip()]
    return {
        'id': user['id'],
        'last_name': user['last_name'],
        'first_name': user['first_name'],
        'email': user['email'],
        'department': user['department'],
        'skills': skills,
        'photo': user['photo'],
        'role': user['role']
    }

# Route to update user profile
@profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
@login_required()  # Restrict to authenticated users
def update_profile(user_id):
    """Update a user's own profile details."""
    current_user_id = int(session['user_id'])
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only update your own profile'}), 403

    user = user_manager.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400

    skills_data = data.get('skills')
    skills = None
    if skills_data is not None:
        skills = skills_data if isinstance(skills_data, list) else [skill.strip() for skill in skills_data.split(',') if skill.strip()]

    update_payload = {}
    if data.get('last_name') is not None: update_payload['last_name'] = data['last_name']
    if data.get('first_name') is not None: update_payload['first_name'] = data['first_name']
    if data.get('department') is not None: update_payload['department'] = data['department']
    if skills is not None: update_payload['skills'] = skills
    if data.get('photo') is not None: update_payload['photo'] = data['photo']
    if data.get('email') is not None: update_payload['email'] = data['email']
    if data.get('password') is not None: update_payload['password'] = data['password']

    # Ignore 'role' to prevent privilege escalation
    if 'role' in data:
        return jsonify({'error': 'Unauthorized: Role cannot be updated via this endpoint'}), 403

    if not update_payload:
        return jsonify({'error': 'No valid fields provided for update'}), 400

    # Update user in database
    success = user_manager.update_user(user_id, **update_payload)
    if success:
        # Log admin action
        log_admin_action(current_user_id, 'update_profile', 'user', user_id, f"Updated fields: {list(update_payload.keys())}")
        
        # Fetch updated user
        updated_user = user_manager.get_user_by_id(user_id)
        serialized_user = serialize_user(updated_user)
        
        return jsonify({
            'message': 'User updated successfully',
            'user': serialized_user
        }), 200

    return jsonify({'error': 'Failed to update user'}), 500


@profile_bp.route('/profile/<int:user_id>', methods=['DELETE'])
@login_required()  # Restrict to authenticated users
def delete_profile(user_id):
    """Delete the authenticated user's own profile."""
    current_user_id = int(session['user_id'])
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own profile'}), 403

    if not user_manager.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    if user_manager.delete_user(user_id):
        log_admin_action(current_user_id, 'delete_profile', 'user', user_id)
        session.clear()  # Clear the session to log the user out
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete user'}), 500

@profile_bp.route('/search', methods=['GET'])
@login_required()
def search_profiles():
    # الحصول على القيم من الاستعلام في الـ URL
    nom = request.args.get('nom', '').strip()
    filiere = request.args.get('filiere', '').strip()
    competence = request.args.get('competence', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # استدعاء دالة البحث مع تمرير المعايير
    profiles, total = user_manager.search_users(
        first_name=nom,  # استبدال "nom" بـ "first_name"
        department=filiere,  # استبدال "filiere" بـ "department"
        skill=competence,  # استبدال "competence" بـ "skill"
        exclude_user_id=session.get('user_id'),
        page=page,
        per_page=per_page
    )
    
    results = []
    for p in profiles:
        competences_list = [c.strip() for c in p['skills'].split(',') if c.strip()] if p['skills'] else []
        results.append({
            'id': p['id'],
            'last_name': p['last_name'],
            'first_name': p['first_name'],
            'email': p['email'],
            'department': p['department'],
            'skills': competences_list,
            'photo': p['photo'],
            'role': p['role']
        })
    
    # إرجاع النتيجة بتنسيق JSON مع معلومات الصفحات
    return jsonify({
        'results': results,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200
