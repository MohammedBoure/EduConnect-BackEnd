import sys
import os
import random
import sqlite3
import logging
from datetime import datetime, timezone

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database.base import Database
from database.comment import CommentManager  # Assuming CommentManager is in database/comment.py

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_users(db_path, user_ids):
    """Create users with given IDs if they don't exist, matching the users table schema."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for user_id in user_ids:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, department, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    f'User{user_id}',
                    f'Lastname{user_id}',
                    f'user{user_id}@example.com',
                    Database.hash_password('password123'),
                    'Computer Science',
                    'user'
                ))
            conn.commit()
            logging.info(f"Users created/verified: {user_ids}")
    except sqlite3.Error as e:
        logging.error(f"Error creating users: {e}")

def create_posts(db_path, post_ids):
    """Create posts with given IDs if they don't exist, matching the posts table schema."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for post_id in post_ids:
                cursor.execute('''
                    INSERT OR IGNORE INTO posts (id, user_id, content, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    post_id,
                    random.choice([8, 10, 12, 13, 16]),  # Random user from the list
                    f'Sample post content for post {post_id}',
                    datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                ))
            conn.commit()
            logging.info(f"Posts created/verified: {post_ids}")
    except sqlite3.Error as e:
        logging.error(f"Error creating posts: {e}")

def create_comments(comment_manager, post_ids, user_ids):
    """Generate 3-15 diverse comments per post by specified users."""
    # Diverse comment templates in English
    comment_templates = [
        "Awesome post! Thanks for sharing!",
        "This is really interesting! Can you elaborate?",
        "Love this content! Keep it coming!",
        "Great insights, well done!",
        "What inspired this post? Curious!",
        "This made me think differently, thanks!",
        "Cool perspective! What's next?",
        "Wow, super engaging!",
        "Thanks for the valuable info!",
        "Learning a lot from this, great job!",
        "This post is fantastic!",
        "Really appreciate this share!",
        "Interesting ideas! More please!",
        "You totally nailed this!",
        "Such a great read!"
    ]

    for post_id in post_ids:
        # Randomly select number of comments between 3 and 15
        num_comments = random.randint(3, 15)
        logging.info(f"Generating {num_comments} comments for post {post_id}")
        
        # Randomly select users for the comments
        selected_users = random.choices(user_ids, k=num_comments)
        
        for user_id in selected_users:
            # Randomly select a comment from the templates
            content = random.choice(comment_templates)
            # Create the comment using CommentManager with created_at=None
            comment_id = comment_manager.create_comment(post_id, user_id, content, created_at=None)
            if comment_id:
                logging.info(f"Comment {comment_id} created for post {post_id} by user {user_id}")
            else:
                logging.error(f"Failed to create comment for post {post_id} by user {user_id}")

if __name__ == "__main__":
    # Database path
    DB_PATH = os.path.join("database", "student_directory.db")
    
    # User IDs and Post IDs
    USER_IDS = [8, 10, 12, 13, 16]
    POST_IDS = [5, 6, 7, 8, 9, 13, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    
    # Initialize CommentManager
    comment_manager = CommentManager()
    
    # Create users and posts
    create_users(DB_PATH, USER_IDS)
    create_posts(DB_PATH, POST_IDS)
    
    # Create comments
    create_comments(comment_manager, POST_IDS, USER_IDS)
    
    # Verify comments were added
    for post_id in POST_IDS:
        comments, total = comment_manager.get_comments_by_post(post_id)
        logging.info(f"Post {post_id} has {total} comments")
        for comment in comments:
            logging.info(f"Comment ID {comment['id']}: From user {comment['user_id']} - {comment['content']}")