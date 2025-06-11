## [1.0.0] - 2025-06-11

### Features
- Added support for retrieving posts by normal users  
  - Introduced a new endpoint `GET /posts/users`
  - Limited post previews to first 101 characters
  - Added helper method `get_normal_user_ids()` in the User DB class

### Improvements
- Enhanced user update flow:
  - Session is cleared if a user updates their own role/profile (forces logout)
  - Improved admin UI by adding an admin page link to the README
  - Renamed "users" and "posts" identifiers to English for clarity

### Fixes
- Resolved CORS preflight issues:
  - Allowed `OPTIONS` requests in `login_required` to prevent 401 errors
  - Enabled `Flask-CORS` with `supports_credentials=True` for cookie-based sessions
  - Added `credentials: include` to frontend fetch requests for session support

### Documentation
- Updated all API documentation to reflect the move from JWT to session-based authentication:
  - `auth.md`, `admin.md`, `comments.md`, `messages.md`, `posts.md`, `profile.md`
- Added **English versions** of all API documentation files alongside the Arabic ones

