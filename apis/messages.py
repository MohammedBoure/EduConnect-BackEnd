from flask import Blueprint, request, jsonify, session
import datetime
from .auth import login_required
from database import MessageManager, AuditLogManager, UserManager

message_manager = MessageManager()
audit_log_manager = AuditLogManager()
user_manager = UserManager()

messages_bp = Blueprint('messages', __name__)

def log_admin_action(admin_id, action, resource_type, resource_id, details=None):
    """Log administrative actions for auditing purposes."""
    audit_log_manager.log_action(admin_id, action, resource_type, resource_id, details)

@messages_bp.route('/messages', methods=['POST'])
@login_required()
def send_message():
    """Send a new message from one user to another."""
    current_user_id = session.get('user_id')
    
    data = request.get_json()
    if not data or not data.get('receiver_id') or not str(data.get('content', '')).strip():
        return jsonify({'error': 'Receiver ID and non-empty content are required.'}), 400

    try:
        receiver_id = int(data['receiver_id'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid receiver_id format'}), 400

    if current_user_id == receiver_id:
        return jsonify({'error': 'Cannot send messages to yourself'}), 400

    if not user_manager.get_user_by_id(receiver_id):
        return jsonify({'error': 'Receiver not found'}), 404

    content = str(data['content']).strip()
    message_id = message_manager.send_message(current_user_id, receiver_id, content)

    if message_id:
        sent_message = message_manager.get_message_by_id(message_id)
        if sent_message:
            msg_data = {
                'id': sent_message['id'],
                'content': sent_message['content'],
                'sender_id': sent_message['sender_id'],
                'receiver_id': sent_message['receiver_id'],
                'created_at': sent_message['created_at'].isoformat() + "Z"
                              if isinstance(sent_message['created_at'], datetime.datetime)
                              else str(sent_message['created_at'])
            }
        else:
            msg_data = {
                'id': message_id,
                'content': content,
                'sender_id': current_user_id,
                'receiver_id': receiver_id,
                'created_at': datetime.datetime.utcnow().isoformat() + "Z"
            }
        return jsonify({'message': 'Message sent successfully', 'sent_message': msg_data}), 201

    return jsonify({'error': 'Failed to send message'}), 500

@messages_bp.route('/messages/<int:other_user_id>', methods=['GET'])
@login_required()
def get_messages(other_user_id):
    """Retrieve messages between two users with pagination."""
    current_user_id = session.get('user_id')

    if not user_manager.get_user_by_id(other_user_id):
        return jsonify({'error': 'Other user not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    messages, total = message_manager.get_messages_between_users(current_user_id, other_user_id, page, per_page)
    messages.reverse()

    message_list = [{
        'id': message['id'],
        'content': message['content'],
        'sender_id': message['sender_id'],
        'receiver_id': message['receiver_id'],
        'created_at': message['created_at'].isoformat() + "Z"
                      if isinstance(message['created_at'], datetime.datetime)
                      else str(message['created_at'])
    } for message in messages]

    return jsonify({
        'messages': message_list,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
        'per_page': per_page
    }), 200
