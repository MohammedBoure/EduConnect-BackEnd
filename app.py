from flask import Flask, session
from flask_cors import CORS
import datetime
from database import UserManager  # Assuming this is your database manager
from apis.auth import auth_bp
from apis.profile_ import profile_bp
from apis.messages import messages_bp
from apis.posts import posts_bp
from apis.comments import comments_bp
from apis.admin import admin_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
            "http://127.0.0.1:5500",
            "https://educonnect-front-end.onrender.com",
            "https://educonnect-admin.onrender.com"
        ]}}, supports_credentials=True)

# Configure secret key for session management
app.config['SECRET_KEY'] = 'your-secret-key-here'  # CHANGE THIS TO A SECURE RANDOM STRING!
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=10)

# Initialize database
user_manager = UserManager()  # This triggers init_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')
app.register_blueprint(messages_bp, url_prefix='/api')
app.register_blueprint(posts_bp, url_prefix='/api')
app.register_blueprint(comments_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)