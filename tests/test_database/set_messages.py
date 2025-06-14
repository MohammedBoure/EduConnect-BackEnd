import sqlite3
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database.message import MessageManager
from database.base import Database

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
                    Database.hash_password('password123'),  # Default password for all users
                    'Computer Science',  # Default department
                    'user'  # Default role
                ))
            conn.commit()
            logging.info(f"Users created/verified: {user_ids}")
    except sqlite3.Error as e:
        logging.error(f"Error creating users: {e}")

def create_conversations(message_manager, user_ids):
    """Create organized conversations between all possible pairs of users."""
    # Generate all unique pairs of users
    pairs = [(user_ids[i], user_ids[j]) for i in range(len(user_ids)) for j in range(i + 1, len(user_ids))]
    
    # Define conversation threads for each pair
    conversation_threads = [
        {
            "participants": (8, 10),
            "topic": "Project Planning",
            "messages": [
                ("Hey, have you started on the project plan yet?", 8),
                ("Not yet, just gathering some ideas. Got any suggestions?", 10),
                ("Let's focus on the timeline first. Maybe a 3-month schedule?", 8),
                ("Sounds good. I'll draft a timeline and share it tomorrow.", 10),
                ("Great! Also, we need to assign roles. Want to handle design?", 8),
                ("Sure, I can take design. You'll cover testing?", 10)
            ]
        },
        {
            "participants": (10, 12),
            "topic": "Study Group",
            "messages": [
                ("Hey, want to join the study group for the exam?", 10),
                ("Definitely! When and where are we meeting?", 12),
                ("How about Thursday, 6 PM at the library?", 10),
                ("Works for me. Should we focus on chapters 1-3?", 12),
                ("Yeah, those are key. I'll bring some practice questions.", 10)
            ]
        },
        {
            "participants": (12, 13),
            "topic": "Event Organization",
            "messages": [
                ("We need to plan the club event. Any ideas?", 12),
                ("Maybe a tech talk? We could invite a guest speaker.", 13),
                ("Good idea! I know someone from a local startup.", 12),
                ("Awesome! I'll handle the venue booking.", 13),
                ("Cool, let's aim for next month. I'll send out invites.", 12)
            ]
        },
        {
            "participants": (13, 16),
            "topic": "Hackathon Prep",
            "messages": [
                ("You in for the hackathon next week?", 13),
                ("Totally! What's our project idea?", 16),
                ("Thinking about a task management app. Thoughts?", 13),
                ("Love it! I can work on the frontend.", 16),
                ("Perfect, I'll handle backend. Let's meet to brainstorm.", 13),
                ("Tomorrow at 3 PM work for you?", 16)
            ]
        },
        {
            "participants": (8, 16),
            "topic": "Group Assignment",
            "messages": [
                ("Hey, we need to finish the group assignment.", 8),
                ("Right, I'm working on the intro. You got the analysis?", 16),
                ("Yeah, almost done. Can you review my section?", 8),
                ("Sure, send it over. I'll check it tonight.", 16),
                ("Thanks! Let's submit by Friday.", 8)
            ]
        },
        {
            "participants": (8, 12),
            "topic": "Code Review Session",
            "messages": [
                ("Hey, can we schedule a code review for our project?", 8),
                ("Sure, I'm free this afternoon. What time?", 12),
                ("How about 2 PM via Zoom?", 8),
                ("Works for me. I'll share my code beforehand.", 12),
                ("Great, I'll review it and send feedback.", 8)
            ]
        },
        {
            "participants": (8, 13),
            "topic": "Research Collaboration",
            "messages": [
                ("Interested in collaborating on a research paper?", 8),
                ("Yeah, what's the topic?", 13),
                ("I'm thinking AI in education. Thoughts?", 8),
                ("Sounds promising. I can help with data analysis.", 13),
                ("Awesome, let's draft an outline this week.", 8)
            ]
        },
        {
            "participants": (10, 13),
            "topic": "Internship Discussion",
            "messages": [
                ("Hey, applied to any internships yet?", 10),
                ("Yeah, just sent one to TechCorp. You?", 13),
                ("Same! How's your application going?", 10),
                ("Got an interview next week. Nervous!", 13),
                ("You'll crush it. Want to practice?", 10)
            ]
        },
        {
            "participants": (10, 16),
            "topic": "Open Source Contribution",
            "messages": [
                ("Thinking of contributing to an open-source project?", 10),
                ("Yeah, I found a cool repo on GitHub. Interested?", 16),
                ("Definitely! What's the project about?", 10),
                ("It's a task scheduler. I can send you the link.", 16),
                ("Cool, let's pick an issue to work on.", 10)
            ]
        },
        {
            "participants": (12, 16),
            "topic": "Workshop Planning",
            "messages": [
                ("We need to organize a Python workshop. Ideas?", 12),
                ("Maybe a beginner-friendly session on data analysis?", 16),
                ("Good call! I can prepare some exercises.", 12),
                ("I'll handle the slides. When should we do it?", 16),
                ("Next Friday works. I'll book a room.", 12)
            ]
        }
    ]

    for thread in conversation_threads:
        sender_id, receiver_id = thread["participants"]
        logging.info(f"Creating conversation: {thread['topic']} between {sender_id} and {receiver_id}")
        for content, sender in thread["messages"]:
            message_manager.send_message(sender, receiver_id if sender == sender_id else sender_id, content)

if __name__ == "__main__":
    # Database path (use os.path for cross-platform compatibility)
    DB_PATH = os.path.join("database", "student_directory.db")
    
    # User IDs provided
    USER_IDS = [8, 10, 12, 13, 16]
    
    # Initialize MessageManager
    message_manager = MessageManager()
    
    # Create users
    create_users(DB_PATH, USER_IDS)
    
    # Create organized conversations
    create_conversations(message_manager, USER_IDS)
    
    # Verify messages were added
    messages, total = message_manager.get_all_messages()
    logging.info(f"Total messages in database: {total}")
    for message in messages:
        logging.info(f"Message ID {message[0]}: From {message[3]} to {message[4]} - {message[1]}")