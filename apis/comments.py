from flask import Blueprint, request, jsonify, session
import datetime
from database import AuditLogManager, CommentManager, PostManager
from dateutil.parser import isoparse
from .auth import login_required

audit_log_manager = AuditLogManager()
comment_manager = CommentManager()
post_manager = PostManager()

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required()
def add_comment(post_id):
    """Add a comment to a post."""
    try:
        if not post_manager.get_post_by_id(post_id):
            return jsonify({'error': 'Post not found'}), 404

        new_comment = request.get_json()
        if 'content' not in new_comment or 'created_at' not in new_comment:
            return jsonify({'error': 'Missing content or created_at field'}), 400

        if 'user_id' in new_comment:
            return jsonify({'error': 'Specifying user_id is not allowed'}), 403

        content = new_comment['content']
        created_at = new_comment['created_at']

        if len(content.strip()) == 0 or len(content) > 1000:
            return jsonify({'error': 'Content must be between 1 and 1000 characters'}), 400

        if isinstance(created_at, str):
            try:
                created_at = isoparse(created_at)
            except ValueError:
                return jsonify({'error': 'Invalid date format for created_at'}), 400
        elif not isinstance(created_at, datetime.datetime):
            return jsonify({'error': 'created_at must be a datetime object or ISO format string'}), 400

        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'error': 'User not authenticated'}), 401

        comment_id = comment_manager.create_comment(
            post_id=post_id,
            user_id=user_id,
            content=content,
            created_at=created_at
        )
        if comment_id:
            comment = comment_manager.get_comment_by_id(comment_id)
            return jsonify({
                'message': 'Comment added successfully',
                'comment': {
                    'id': comment['id'],
                    'content': comment['content'],
                    'created_at': comment['created_at'].isoformat() + "Z",
                    'post_id': comment['post_id'],
                    'user_id': comment['user_id']
                }
            }), 201
        return jsonify({'error': 'Failed to create comment'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """Get comments for a post."""
    if not post_manager.get_post_by_id(post_id):
        return jsonify({'error': 'Post not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    comments, total = comment_manager.get_comments_by_post(post_id, page, per_page)

    comment_list = []
    for c in comments:
        comment_data = {
            'id': c['id'],
            'content': c['content'],
            'created_at': c['created_at'].isoformat() + "Z" if isinstance(c['created_at'], datetime.datetime) else str(c['created_at']),
            'post_id': c['post_id'],
            'user_id': c['user_id'],
            'author': {
                'first_name': c['first_name'],
                'last_name': c['last_name'],
                'photo': c['photo']
            }
        }
        comment_list.append(comment_data)

    return jsonify({
        'comments': comment_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200

@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@login_required()
def update_comment(comment_id):
    """Update an existing comment."""
    comment = comment_manager.get_comment_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    data = request.get_json()
    content = data.get('content', '').strip() if data else ''
    if not content:
        return jsonify({'error': 'Comment content cannot be empty'}), 400

    if comment_manager.update_comment(comment_id, content):
        admin_id = session.get('user_id', 0)
        log_admin_action(admin_id, 'update_comment', 'comment', comment_id, f"New content: {content[:50]}...")
        updated_comment = comment_manager.get_comment_by_id(comment_id)
        

        created_at_iso = ""
        if isinstance(updated_comment['created_at'], datetime.datetime):
            created_at_iso = updated_comment['created_at'].isoformat() + "Z"
        else:
            created_at_iso = str(updated_comment['created_at'])

        comment_data = {
            'id': updated_comment['id'],
            'content': updated_comment['content'],
            'created_at': created_at_iso,
            'post_id': updated_comment['post_id'],
            'user_id': updated_comment['user_id'],
            'author': {
                'last_name': updated_comment['last_name'],
                'first_name': updated_comment['first_name'],
                'photo': updated_comment['photo']
            }
        }

        
        return jsonify({'message': 'Comment updated successfully', 'comment': comment_data}), 200
    return jsonify({'error': 'Failed to update comment'}), 500

@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required()
def delete_comment(comment_id):
    """Delete a comment by ID."""
    if session.get('user_id') is None:
        return jsonify({'error': 'User not authenticated'}), 401

    if not comment_manager.get_comment_by_id(comment_id):
        return jsonify({'error': 'Comment not found'}), 404

    if comment_manager.delete_comment(comment_id):
        admin_id = session.get('user_id', 0)
        log_admin_action(admin_id, 'delete_comment', 'comment', comment_id)
        return jsonify({'message': 'Comment deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete comment'}), 500