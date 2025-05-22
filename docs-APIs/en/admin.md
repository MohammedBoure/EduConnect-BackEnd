# Admin APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a test environment.

## Overview
The Admin APIs provide tools for managing users, posts, comments, and messages. These APIs are restricted to users with administrative privileges (role `admin`) and require an active session to access most endpoints.

## Prerequisites
- **Server**: Runs on `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: An active session with the `admin` role is required for most endpoints, except for `OPTIONS` requests.
- **Content Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.
- **Sessions**: Sessions are used to track login state. Browsers must support cookies for session management.

## Endpoints

### 1. Retrieve User List
- **Method**: `GET`, `OPTIONS`
- **URL**: `/admin/users`
- **Description**: Retrieve a paginated list of users.
- **Authentication**: Not required for `OPTIONS` requests, required (role `admin`) for `GET` requests.

#### Query Parameters
| Parameter  | Type    | Description              | Default |
| ---------- | ------- | ------------------------ | ------- |
| `page`     | Integer | Page number              | 1       |
| `per_page` | Integer | Number of users per page | 10      |

#### Responses
- **200 OK**:
  ```json
  {
    "users": [
      {
        "id": 1,
        "last_name": "Benali",
        "first_name": "Ahmed",
        "email": "ahmed.benali@example.com",
        "department": "Computer Science",
        "skills": ["Python", "JavaScript"],
        "photo": "https://example.com/photos/ahmed.jpg",
        "role": "user"
      }
    ],
    "total": 50,
    "page": 1,
    "pages": 5,
    "per_page": 10
  }
  ```

#### Example JavaScript (Frontend):
```javascript
async function listUsers(page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/users?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch users');
    }
    console.log('Users fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
listUsers(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Retrieve User Profile
- **Method**: `GET`, `OPTIONS`
- **URL**: `/admin/users/<user_id>`
- **Description**: Retrieve details of a specific user by ID.
- **Authentication**: Not required for `OPTIONS` requests, required (role `admin`) for `GET` requests.

#### Responses
- **200 OK**:
  ```json
  {
    "id": 1,
    "last_name": "Benali",
    "first_name": "Ahmed",
    "email": "ahmed.benali@example.com",
    "department": "Computer Science",
    "skills": ["Python", "JavaScript"],
    "photo": "https://example.com/photos/ahmed.jpg",
    "role": "user"
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function getUserProfile(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/users/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch user profile');
    }
    console.log('User profile fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getUserProfile(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. Update User Profile
- **Method**: `PUT`
- **URL**: `/admin/users/<user_id>`
- **Description**: Update a user’s details, including their role.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field        | Type         | Description         | Notes                             |
| ------------ | ------------ | ------------------- | --------------------------------- |
| `first_name` | String       | First name          | Optional                          |
| `last_name`  | String       | Last name           | Optional                          |
| `email`      | String       | Email address       | Optional, must be valid           |
| `password`   | String       | Password            | Optional, minimum 8 characters    |
| `department` | String       | Department/Major    | Optional                          |
| `skills`     | String/Array | Skills              | Optional, comma-separated or list |
| `photo`      | String       | Profile picture URL | Optional                          |
| `role`       | String       | User role           | Optional, `user` or `admin`       |

**Example**:
```json
{
  "first_name": "Ahmed",
  "last_name": "Benali",
  "email": "ahmed.benali@example.com",
  "password": "newpassword123",
  "department": "Computer Science",
  "skills": ["Python", "JavaScript"],
  "photo": "https://example.com/photos/ahmed.jpg",
  "role": "admin"
}
```

#### Responses
- **200 OK**:
  ```json
  {
    "message": "User updated successfully",
    "user": {
      "id": 1,
      "last_name": "Benali",
      "first_name": "Ahmed",
      "email": "ahmed.benali@example.com",
      "department": "Computer Science",
      "skills": ["Python", "JavaScript"],
      "photo": "https://example.com/photos/ahmed.jpg",
      "role": "admin"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "No update data provided"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "No valid fields provided for update"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update user"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function updateUserProfile(userId, userData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update user');
    }
    console.log('User updated successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const userData = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'newpassword123',
  department: 'Computer Science',
  skills: ['Python', 'JavaScript'],
  photo: 'https://example.com/photos/ahmed.jpg',
  role: 'admin'
};

updateUserProfile(1, userData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. Delete User
- **Method**: `DELETE`
- **URL**: `/admin/users/<user_id>`
- **Description**: Delete a user by ID.
- **Authentication**: Required (role `admin`).

#### Responses
- **200 OK**:
  ```json
  {"message": "User deleted successfully"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete user"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function deleteUser(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/users/${userId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete user');
    }
    console.log('User deleted successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
deleteUser(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 5. Create Post
- **Method**: `POST`
- **URL**: `/admin/posts/create`
- **Description**: Create a new post on behalf of a user.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field       | Type    | Description            | Notes           |
| ----------- | ------- | ---------------------- | --------------- |
| `user_id` * | Integer | ID of the post creator | Required        |
| `title` *   | String  | Post title             | Cannot be empty |
| `content` * | String  | Post content           | Cannot be empty |
| `image`     | String  | Image URL              | Optional        |

**Example**:
```json
{
  "user_id": 1,
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
  {"error": "Missing user_id"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Title and content cannot be empty"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create post"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function createPost(postData) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/admin/posts/create', {
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
  user_id: 1,
  title: 'New Project Announcement',
  content: 'We are excited to announce a new project...',
  image: 'https://example.com/images/project.jpg'
};

createPost(postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 6. Retrieve Post List
- **Method**: `GET`, `OPTIONS`
- **URL**: `/admin/posts`
- **Description**: Retrieve a paginated list of posts.
- **Authentication**: Not required for `OPTIONS` requests, required (role `admin`) for `GET` requests.

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

#### Example JavaScript (Frontend):
```javascript
async function listPosts(page = 1, perPage = 10) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/posts?page=${page}&per_page=${perPage}`, {
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
listPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 7. Update Post
- **Method**: `PUT`
- **URL**: `/admin/posts/<post_id>`
- **Description**: Update an existing post.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field     | Type   | Description  | Notes                                 |
| --------- | ------ | ------------ | ------------------------------------- |
| `title`   | String | Post title   | Optional, cannot be empty if provided |
| `content` | String | Post content | Optional, cannot be empty if provided |
| `image`   | String | Image URL    | Optional                              |

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
  {"error": "Title and content cannot be empty"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update post"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function updatePost(postId, postData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/posts/${postId}`, {
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
- **URL**: `/admin/posts/<post_id>`
- **Description**: Delete a post by ID.
- **Authentication**: Required (role `admin`).

#### Responses
- **200 OK**:
  ```json
  {"message": "Post deleted successfully"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Post not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete post"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function deletePost(postId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/posts/${postId}`, {
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

### 9. Add Comment
- **Method**: `POST`
- **URL**: `/admin/posts/<post_id>/comments`
- **Description**: Add a comment to a post.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field          | Type            | Description         | Notes                         |
| -------------- | --------------- | ------------------- | ----------------------------- |
| `content` *    | String          | Comment content     | Cannot be empty               |
| `created_at` * | String/Datetime | Creation date/time  | ISO format or datetime object |
| `user_id` *    | Integer         | Commenter’s user ID | Required                      |

**Example**:
```json
{
  "content": "Great project, looking forward to more updates!",
  "created_at": "2025-05-22T07:28:00Z",
  "user_id": 1
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
  {"error": "Missing content, created_at, or user_id field"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid date format for created_at"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to create comment"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function addComment(postId, commentData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/posts/${postId}/comments`, {
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
  created_at: '2025-05-22T07:28:00Z',
  user_id: 1
};

addComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 10. Retrieve Comment List
- **Method**: `GET`, `OPTIONS`
- **URL**: `/admin/comments`
- **Description**: Retrieve a paginated list of comments.
- **Authentication**: Not required for `OPTIONS` requests, required (role `admin`) for `GET` requests.

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
          "last_name": "Benali",
          "first_name": "Ahmed",
          "photo": "https://example.com/photos/ahmed.jpg"
        }
      }
    ],
    "total": 100,
    "page": 1,
    "pages": 5,
    "per_page": 20
  }
  ```

#### Example JavaScript (Frontend):
```javascript
async function listComments(page = 1, perPage = 20) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/comments?page=${page}&per_page=${perPage}`, {
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
listComments(1, 20)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 11. Update Comment
- **Method**: `PUT`
- **URL**: `/admin/comments/<comment_id>`
- **Description**: Update an existing comment.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field       | Type   | Description     | Notes           |
| ----------- | ------ | --------------- | --------------- |
| `content` * | String | Comment content | Cannot be empty |

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
        "last_name": "Benali",
        "first_name": "Ahmed",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "No data provided"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Comment content cannot be empty"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update comment"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function updateComment(commentId, commentData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/comments/${commentId}`, {
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

### 12. Delete Comment
- **Method**: `DELETE`, `OPTIONS`
- **URL**: `/admin/comments/<comment_id>`
- **Description**: Delete a comment by ID.
- **Authentication**: Required (role `admin`) for `DELETE` requests.

#### Responses
- **200 OK**:
  ```json
  {"message": "Comment deleted successfully"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Comment not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete comment"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function deleteComment(commentId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/comments/${commentId}`, {
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

### 13. Retrieve Message List
- **Method**: `GET`, `OPTIONS`
- **URL**: `/admin/messages`
- **Description**: Retrieve a paginated list of messages.
- **Authentication**: Not required for `OPTIONS` requests, required (role `admin`) for `GET` requests.

#### Query Parameters
| Parameter  | Type    | Description                 | Default |
| ---------- | ------- | --------------------------- | ------- |
| `page`     | Integer | Page number                 | 1       |
| `per_page` | Integer | Number of messages per page | 30      |

#### Responses
- **200 OK**:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "content": "Hello, how's the project going?",
        "sender_id": 1,
        "receiver_id": 2,
        "created_at": "2025-05-22T07:28:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "pages": 4,
    "per_page": 30
  }
  ```

#### Example JavaScript (Frontend):
```javascript
async function listMessages(page = 1, perPage = 30) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/messages?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch messages');
    }
    console.log('Messages fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
listMessages(1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 14. Send Message
- **Method**: `POST`
- **URL**: `/admin/messages`
- **Description**: Send a new message from one user to another.
- **Authentication**: Required (role `admin`).

#### Request Body
| Field           | Type    | Description     | Notes           |
| --------------- | ------- | --------------- | --------------- |
| `sender_id` *   | Integer | Sender ID       | Required        |
| `receiver_id` * | Integer | Receiver ID     | Required        |
| `content` *     | String  | Message content | Cannot be empty |

**Example**:
```json
{
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hello, how's the project going?"
}
```

#### Responses
- **201 Created**:
  ```json
  {
    "message": "Message sent successfully",
    "sent_message": {
      "id": 1,
      "content": "Hello, how's the project going?",
      "sender_id": 1,
      "receiver_id": 2,
      "created_at": "2025-05-22T07:28:00Z"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Sender ID, receiver ID, and non-empty content are required"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid sender_id or receiver_id format"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Cannot send messages to yourself"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Receiver not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to send message"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function sendMessage(messageData) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/admin/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(messageData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    console.log('Message sent successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const messageData = {
  sender_id: 1,
  receiver_id: 2,
  content: "Hello, how's the project going?"
};

sendMessage(messageData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 15. Delete Message
- **Method**: `DELETE`
- **URL**: `/admin/messages/<message_id>`
- **Description**: Delete a message by ID.
- **Authentication**: Required (role `admin`).

#### Responses
- **200 OK**:
  ```json
  {"message": "Message deleted successfully"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Message not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete message"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function deleteMessage(messageId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/messages/${messageId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete message');
    }
    console.log('Message deleted successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
deleteMessage(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 16. Retrieve Messages Between Users
- **Method**: `GET`
- **URL**: `/admin/messages/<current_user_id>/<other_user_id>`
- **Description**: Retrieve messages between two users, paginated.
- **Authentication**: Required (role `admin`).

#### Query Parameters
| Parameter  | Type    | Description                 | Default |
| ---------- | ------- | --------------------------- | ------- |
| `page`     | Integer | Page number                 | 1       |
| `per_page` | Integer | Number of messages per page | 30      |

#### Responses
- **200 OK**:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "content": "Hello, how's the project going?",
        "sender_id": 1,
        "receiver_id": 2,
        "created_at": "2025-05-22T07:28:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "pages": 2,
    "per_page": 30
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "Other user not found"}
  ```
- **404 Not Found**:
  ```json
  {"error": "Current user not found"}
  ```
- **404 Not Found**:
  ```json
  {"error": "No messages found"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function getMessages(currentUserId, otherUserId, page = 1, perPage = 30) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/admin/messages/${currentUserId}/${otherUserId}?page=${page}&per_page=${perPage}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch messages');
    }
    console.log('Messages fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
getMessages(1, 2, 1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to secure sensitive data.
- Test APIs using tools like Postman or cURL.
- Cookies must be enabled in the browser to support session management.
- For APIs requiring authentication, an active session with `user_id` and `role` set to `admin` is verified.
- All administrative actions (e.g., updating or deleting users, posts, comments, or messages) are logged using `AuditLogManager` for auditing purposes.
- For enhanced security, ensure session cookies are sent with `HttpOnly` and `Secure` attributes in production.
- Session duration depends on the server’s `PERMANENT_SESSION_LIFETIME` configuration.