# Comments APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a testing environment.

## Overview
The Comments APIs provide tools for managing comments on posts, including adding new comments, retrieving comments, updating comments, and deleting them. Most endpoints require an active user session for authentication.

## Prerequisites
- **Server**: Running at `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: Users must have an active session (with `user_id` in the session) to access endpoints requiring authentication, except for retrieving comments.
- **Content Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.
- **Sessions**: Sessions are used to track login status. Browsers must support cookies for session management.

## Endpoints

### 1. Add Comment
- **Method**: `POST`
- **URL**: `/posts/<post_id>/comments`
- **Description**: Add a new comment to a specific post.
- **Authentication**: Required (active user session).

#### Request Body
| Field          | Type            | Description            | Notes                                |
| -------------- | --------------- | ---------------------- | ------------------------------------ |
| `content` *    | String          | Comment content        | Cannot be empty, max 1000 characters |
| `created_at` * | String/Datetime | Creation date and time | ISO format or datetime object        |

**Note**: The `user_id` field is not allowed in the request body, as it is automatically retrieved from the session.

**Example**:
```json
{
  "content": "Great project, looking forward to more updates!",
  "created_at": "2025-05-22T07:28:00Z"
}
```

#### Responses
- **201 Created**:
  ```json
  {
    "message": "Comment added successfully",
    "comment": {
      "id": 1,
      "content": "Great project, looking forward to more updates!",
      "created_at": "2025-05-22T07:28:00Z",
      "post_id": 1,
      "user_id": 1
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Missing content or created_at field"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Content must be between 1 and 1000 characters"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid date format for created_at"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "User not authenticated"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Specifying user_id is not allowed"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create comment"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function addComment(postId, commentData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(commentData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to add comment');
    }
    console.log('Comment added successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const commentData = {
  content: 'Great project, looking forward to more updates!',
  created_at: '2025-05-22T07:28:00Z'
};

addComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Retrieve Post Comments
- **Method**: `GET`
- **URL**: `/posts/<post_id>/comments`
- **Description**: Retrieve a paginated list of comments for a specific post.
- **Authentication**: Not required.

#### Query Parameters
| Parameter  | Type    | Description                 | Default |
| ---------- | ------- | --------------------------- | ------- |
| `page`     | Integer | Page number                 | 1       |
| `per_page` | Integer | Number of comments per page | 20      |

#### Responses
- **200 OK**:
  ```json
  {
    "comments": [
      {
        "id": 1,
        "content": "Great project, looking forward to more updates!",
        "created_at": "2025-05-22T07:28:00Z",
        "post_id": 1,
        "user_id": 1,
        "author": {
          "first_name": "Ahmed",
          "last_name": "Benali",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 50,
    "page": 1,
    "pages": 3,
    "per_page": 20
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function getComments(postId, page = 1, perPage = 20) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}/comments?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch comments');
    }
    console.log('Comments fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getComments(1, 1, 20)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. Update Comment
- **Method**: `PUT`
- **URL**: `/comments/<comment_id>`
- **Description**: Update the content of an existing comment.
- **Authentication**: Required (active user session).

#### Request Body
| Field       | Type   | Description         | Notes           |
| ----------- | ------ | ------------------- | --------------- |
| `content` * | String | New comment content | Cannot be empty |

**Example**:
```json
{
  "content": "Updated comment content"
}
```

#### Responses
- **200 OK**:
  ```json
  {
    "message": "Comment updated successfully",
    "comment": {
      "id": 1,
      "content": "Updated comment content",
      "created_at": "2025-05-22T07:28:00Z",
      "post_id": 1,
      "user_id": 1,
      "author": {
        "first_name": "Ahmed",
        "last_name": "Benali",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Comment content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "User not authenticated"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update comment"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function updateComment(commentId, commentData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/comments/${commentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(commentData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update comment');
    }
    console.log('Comment updated successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const commentData = {
  content: 'Updated comment content'
};

updateComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. Delete Comment
- **Method**: `DELETE`
- **URL**: `/comments/<comment_id>`
- **Description**: Delete a comment by its ID.
- **Authentication**: Required (active user session).

#### Responses
- **200 OK**:
  ```json
  {"message": "Comment deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "User not authenticated"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete comment"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function deleteComment(commentId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/comments/${commentId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete comment');
    }
    console.log('Comment deleted successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
deleteComment(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to secure sensitive data.
- Test the APIs using tools like Postman or cURL.
- Browser cookies must be enabled to support session management.
- For APIs requiring authentication, the presence of an active session with a `user_id` is validated.
- Actions related to updating or deleting comments are logged using `AuditLogManager` for auditing purposes.
- For enhanced security, ensure session cookies are sent with `HttpOnly` and `Secure` attributes in production.
- Session duration depends on the server's `PERMANENT_SESSION_LIFETIME` configuration.
- Comment content is validated to be between 1 and 1000 characters, and the `user_id` field is rejected in the request body as the user is determined from the session.