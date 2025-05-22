# EduConnect API Documentation

## Fixed Site URL
https://educonnect-admin.onrender.com

- **[Arabic README File](./docs-APIs/ar/README.md)**

## Overview
The EduConnect API is a RESTful interface built using the Flask framework, designed for a social platform managing users, profiles, posts, comments, messages, and administrative tasks. It uses **session-based authentication** and relies on an SQLite database (`student_directory.db`) for data storage. The API supports user registration, login, profile management, messaging, posts, comments, and administrative operations.

## API Documentation
**For Developers**: The detailed documentation is designed to serve as a primary reference for front-end development. You can find all details about endpoints, request types, and response examples in the following documentation files within the `docs-APIs/` directory, available in both English (`en/`) and Arabic (`ar/`) versions:

- **[Admin APIs Documentation (English)](./docs-APIs/en/admin.md)** / **[Arabic](./docs-APIs/ar/admin.md)**: Managing users, posts, comments, and messages (restricted to users with the "admin" role).
- **[Authentication APIs Documentation (English)](./docs-APIs/en/auth.md)** / **[Arabic](./docs-APIs/ar/auth.md)**: User registration and login.
- **[Comments APIs Documentation (English)](./docs-APIs/en/comments.md)** / **[Arabic](./docs-APIs/ar/comments.md)**: Adding, viewing, updating, and deleting comments.
- **[Messages APIs Documentation (English)](./docs-APIs/en/messages.md)** / **[Arabic](./docs-APIs/ar/messages.md)**: Sending and retrieving messages between users.
- **[Posts APIs Documentation (English)](./docs-APIs/en/posts.md)** / **[Arabic](./docs-APIs/ar/posts.md)**: Creating, viewing, updating, and deleting posts.
- **[Profile APIs Documentation (English)](./docs-APIs/en/profile.md)** / **[Arabic](./docs-APIs/ar/profile.md)**: Managing user profiles and searching for users.
- **[Database Documentation (English)](./docs-APIs/en/database.md)** / **[Arabic](./docs-APIs/ar/database.md)**: Explanation of the database structure, tables, and their relationships.

> **Note for Front-End Developers**: Review these files to understand how to interact with the backend, including data structures, response codes (e.g., 200, 401, 404), and request examples using cURL.

## Project Structure
```
├── apis/
│   ├── admin.py          # Admin endpoints for managing users, posts, comments, and messages
│   ├── auth.py           # Authentication endpoints (registration, login)
│   ├── comments.py       # Comment-related endpoints
│   ├── messages.py       # Messaging endpoints
│   ├── posts.py          # Post-related endpoints
│   └── profile_.py       # Profile management and user search endpoints
├── database/
│   ├── __init__.py       # Database initialization
│   ├── audit.py          # Audit logging utilities
│   ├── base.py           # Core database setup
│   ├── comment.py        # Comment model
│   ├── message.py        # Message model
│   ├── post.py           # Post model
│   ├── student_directory.db  # SQLite database
│   └── user.py           # User model
├── docs-APIs/
│   ├── ar/
│   │   ├── README.md     # Arabic README
│   │   ├── admin.md      # Arabic Admin APIs documentation
│   │   ├── auth.md       # Arabic Authentication APIs documentation
│   │   ├── comments.md   # Arabic Comments APIs documentation
│   │   ├── database.md   # Arabic Database structure documentation
│   │   ├── messages.md   # Arabic Messages APIs documentation
│   │   ├── posts.md      # Arabic Posts APIs documentation
│   │   └── profile.md    # Arabic Profile APIs documentation
│   └── en/
│       ├── admin.md      # English Admin APIs documentation
│       ├── auth.md       # English Authentication APIs documentation
│       ├── comments.md   # English Comments APIs documentation
│       ├── database.md   # English Database structure documentation
│       ├── messages.md   # English Messages APIs documentation
│       ├── posts.md      # English Posts APIs documentation
│       └── profile.md    # English Profile APIs documentation
├── Procfile              # Deployment configuration (e.g., for Render)
├── README.md             # Project overview (this file)
├── app.py                # Main Flask application
├── commit                # Commit-related file
├── requirements.txt      # Software dependencies
└── utils.py              # Helper functions
```

## Backend Server
- **Production**: `https://educonnect-wp9t.onrender.com`
- **Local Testing**: `http://127.0.0.1:5000`

## API Features
- **Authentication**: User registration and login using session-based authentication.
- **Profile Management**: View, update, delete, and search user profiles.
- **Posts**: Create, view, update, and delete posts.
- **Comments**: Add, view, update, and delete comments on posts.
- **Messages**: Send and retrieve messages between users.
- **Administrative Operations**: Full control over users, posts, comments, and messages (requires "admin" role).

## Prerequisites
- Python 3.8 or higher
- SQLite database (`student_directory.db`)
- Dependencies listed in `requirements.txt`

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the API at `http://127.0.0.1:5000` or the deployed URL.

## Testing
Use tools like **Postman**, **cURL**, or custom scripts to test the API. Refer to the documentation in `docs-APIs/` for details on endpoints, request formats, and response examples.

## Security
- Use HTTPS in production to protect sensitive data.
- Ensure secure session management in your environment.
- Ensure passwords are encrypted (e.g., using `bcrypt`).

## Deployment
The API is deployed on Render (`https://educonnect-wp9t.onrender.com`). Use the `Procfile` for deployment configurations.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to report bugs or suggest improvements.