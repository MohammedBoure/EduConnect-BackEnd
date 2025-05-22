# Posts APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a testing environment.

## Overview
The Posts APIs provide tools for managing posts, including creating new posts, retrieving posts (for users, admins, or all posts), updating posts, and deleting them. Some endpoints require an active user session for authentication, while others are publicly accessible.

## Prerequisites
- **Server**: Running at `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: Users must have an active session (with `user_id` in the session) to access endpoints requiring authentication (e.g., creating, updating, or deleting posts).
- **Content Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.
- **Sessions**: Sessions are used to track login status. Browsers must support cookies for session management.

## Endpoints

### 1. Create Post
- **Method**: `POST`
- **URL**: `/posts`
- **Description**: Create a new post for the authenticated user.
- **Authentication**: Required (active user session).

#### Request Body
| Field       | Type   | Description  | Notes           |
| ----------- | ------ | ------------ | --------------- |
| `title` *   | String | Post title   | Cannot be empty |
| `content` * | String | Post content | Cannot be empty |
| `image`     | String | Image URL    | Optional        |

**Example**:
```json
{
  "title": "New Project Announcement",
  "content": "We are excited to announce a new project...",
  "image": "https://example.com/images/project.jpg"
}
```

#### Responses
- **201 Created**:
  ```json
  {
    "message": "Post created successfully",
    "post": {
      "id": 1,
      "title": "New Project Announcement",
      "content": "We are excited to announce a new project...",
      "image": "https://example.com/images/project.jpg",
      "created_at": "2025-05-22T07:28:00Z",
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
  {"error": "Invalid request data"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Title and content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Unauthorized: No active session"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create post"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function createPost(postData) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create post');
    }
    console.log('Post created successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const postData = {
  title: 'New Project Announcement',
  content: 'We are excited to announce a new project...',
  image: 'https://example.com/images/project.jpg'
};

createPost(postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Retrieve Specific Post
- **Method**: `GET`, `OPTIONS`
- **URL**: `/posts/<post_id>`
- **Description**: Retrieve a single post by its ID (publicly accessible).
- **Authentication**: Not required.

#### Responses
- **200 OK**:
  ```json
  {
    "post": {
      "id": 1,
      "title": "New Project Announcement",
      "content": "We are excited to announce a new project...",
      "image": "https://example.com/images/project.jpg",
      "created_at": "2025-05-22T07:28:00Z",
      "user_id": 1,
      "author": {
        "first_name": "Ahmed",
        "last_name": "Benali",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function getPost(postId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch post');
    }
    console.log('Post fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getPost(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. Retrieve User Posts
- **Method**: `GET`
- **URL**: `/posts/user/<user_id>`
- **Description**: Retrieve a paginated list of posts for a specific user (publicly accessible).
- **Authentication**: Not required.

#### Query Parameters
| Parameter  | Type    | Description              | Default |
| ---------- | ------- | ------------------------ | ------- |
| `page`     | Integer | Page number              | 1       |
| `per_page` | Integer | Number of posts per page | 10      |

#### Responses
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "New Project Announcement",
        "content": "We are excited to announce a new project...",
        "image": "https://example.com/images/project.jpg",
        "created_at": "2025-05-22T07:28:00Z",
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
    "pages": 5,
    "per_page": 10
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function getUserPosts(userId, page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/user/${userId}?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch user posts');
    }
    console.log('User posts fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getUserPosts(1, 1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. Retrieve Admin User Posts
- **Method**: `GET`, `OPTIONS`
- **URL**: `/posts/admin_user_posts`
- **Description**: Retrieve a paginated list of posts by users with admin roles (publicly accessible).
- **Authentication**: Not required.

#### Query Parameters
| Parameter  | Type    | Description              | Default |
| ---------- | ------- | ------------------------ | ------- |
| `page`     | Integer | Page number              | 1       |
| `per_page` | Integer | Number of posts per page | 10      |

#### Responses
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "Admin Project Update",
        "content": "Important update for the admin team...",
        "image": "https://example.com/images/admin_project.jpg",
        "created_at": "2025-05-22T07:28:00Z",
        "user_id": 1,
        "author": {
          "first_name": "Ahmed",
          "last_name": "Benali",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 20,
    "page": 1,
    "pages": 2,
    "per_page": 10
  }
  ```

#### JavaScript Example (Frontend):
```javascript
async function getAdminUserPosts(page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/admin_user_posts?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch admin posts');
    }
    console.log('Admin posts fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getAdminUserPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 5. Retrieve All Users' Posts
- **Method**: `GET`, `OPTIONS`
- **URL**: `/posts/users_posts`
- **Description**: Retrieve a paginated list of posts by all users (publicly accessible).
- **Authentication**: Not required.

#### Query Parameters
| Parameter  | Type    | Description              | Default |
| ---------- | ------- | ------------------------ | ------- |
| `page`     | Integer | Page number              | 1       |
| `per_page` | Integer | Number of posts per page | 10      |

#### Responses
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "New Project Announcement",
        "content": "We are excited to announce a new project...",
        "image": "https://example.com/images/project.jpg",
        "created_at": "2025-05-22T07:28:00Z",
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
    "pages": 5,
    "per_page": 10
  }
  ```

#### JavaScript Example (Frontend):
```javascript
async function getAllUsersPosts(page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/users_posts?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch users posts');
    }
    console.log('Users posts fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getAllUsersPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 6. Retrieve All Posts
- **Method**: `GET`, `OPTIONS`
- **URL**: `/posts`
- **Description**: Retrieve a paginated list of all posts (publicly accessible).
- **Authentication**: Not required.

#### Query Parameters
| Parameter  | Type    | Description              | Default |
| ---------- | ------- | ------------------------ | ------- |
| `page`     | Integer | Page number              | 1       |
| `per_page` | Integer | Number of posts per page | 10      |

#### Responses
- **200 OK**:
  ```json
  {
    "posts": [
      {
        "id": 1,
        "title": "New Project Announcement",
        "content": "We are excited to announce a new project...",
        "image": "https://example.com/images/project.jpg",
        "created_at": "2025-05-22T07:28:00Z",
        "user_id": 1,
        "author": {
          "first_name": "Ahmed",
          "last_name": "Benali",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 100,
    "page": 1,
    "pages": 10,
    "per_page": 10
  }
  ```

#### JavaScript Example (Frontend):
```javascript
async function getAllPosts(page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch posts');
    }
    console.log('Posts fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getAllPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 7. Update Post
- **Method**: `PUT`
- **URL**: `/posts/<post_id>`
- ** Trip Description**: Update an existing post (only for the post owner or admins).
- **Authentication**: Required (active user session).

#### Request Body
| Field       | Type   | Description  | Notes           |
| ----------- | ------ | ------------ | --------------- |
| `title` *   | String | Post title   | Cannot be empty |
| `content` * | String | Post content | Cannot be empty |
| `image`     | String | Image URL    | Optional        |

**Example**:
```json
{
  "title": "Updated Project Announcement",
  "content": "Updated content for the project announcement...",
  "image": "https://example.com/images/updated_project.jpg"
}
```

#### Responses
- **200 OK**:
  ```json
  {
    "message": "Post updated successfully",
    "post": {
      "id": 1,
      "title": "Updated Project Announcement",
      "content": "Updated content for the project announcement...",
      "image": "https://example.com/images/updated_project.jpg",
      "created_at": "2025-05-22T07:28:00Z",
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
  {"error": "Invalid request data"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Title and content cannot be empty"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Unauthorized: No active session"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Forbidden: You can only update your own posts"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update post"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function updatePost(postId, postData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
    throw new Error(data.error || 'Failed to update post');
    }
    console.log('Post updated successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const postData = {
  title: 'Updated Project Announcement',
  content: 'Updated content for the project announcement...',
  image: 'https://example.com/images/updated_project.jpg'
};

updatePost(1, postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 8. Delete Post
- **Method**: `DELETE`
- **URL**: `/posts/<post_id>`
- **Description**: Delete a post by its ID (only for admins).
- **Authentication**: Required (active user session).

#### Responses
- **200 OK**:
  ```json
  {"message": "Post deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Unauthorized: No active session"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete post"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function deletePost(postId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete post');
    }
    console.log('Post deleted successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
deletePost(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to secure sensitive data.
- Test the APIs using tools like Postman or cURL.
- Browser cookies must be enabled to support session management.
- For APIs requiring authentication, the presence of an active session with a `user_id` is validated.
- Actions related to creating, updating, and deleting posts are logged using `AuditLogManager` for auditing purposes.
- For enhanced security, ensure session cookies are sent with `HttpOnly` and `Secure` attributes in production.
- Session duration depends on the server's `PERMANENT_SESSION_LIFETIME` configuration.
- The `/posts/<post_id>` (GET) endpoint is duplicated in the code (`get_post` and `get_post_by_id`). It is documented once as it is publicly accessible and returns the same data.
- Updating posts is restricted to the post owner or users with the `admin` role.
- Deleting posts is only available to admins, as specified in the endpoint description.