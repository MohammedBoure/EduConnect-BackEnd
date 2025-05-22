# Profile APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a test environment.

## Overview
The Profile APIs allow retrieving, updating, deleting, and searching for user profiles based on specified criteria.

## Prerequisites
- **Server**: Running at `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: Required (JWT) for updating, deleting, and searching profiles.
- **Content-Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.

## Endpoints

### 1. Retrieve User Profile
- **Method**: `GET`
- **URL**: `/api/profile/<user_id>`
- **Description**: Retrieve the profile data of a specific user by ID.
- **Authentication**: Not required.

#### Path Parameters
| Parameter   | Type    | Description     | Notes            |
| ----------- | ------- | --------------- | ---------------- |
| `user_id` * | Integer | User identifier | Positive integer |

#### Responses
- **200 OK**:
  ```json
  {
    "id": 123,
    "last_name": "Ali",
    "first_name": "Ahmed",
    "email": "ahmed.ali@example.com",
    "department": "Computer Science",
    "skills": ["Python", "JavaScript", "React"],
    "photo": "https://example.com/photos/ahmed.jpg",
    "role": "user"
  }
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function getUserProfile(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to retrieve profile');
    }
    console.log('Profile retrieved:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const userId = 123;
getUserProfile(userId)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Update User Profile
- **Method**: `PUT`
- **URL**: `/api/profile/<user_id>`
- **Description**: Update a user’s profile data.
- **Authentication**: Required (JWT, only the profile owner).

#### Path Parameters
| Parameter   | Type    | Description     | Notes            |
| ----------- | ------- | --------------- | ---------------- |
| `user_id` * | Integer | User identifier | Positive integer |

#### Request Body
| Field        | Type         | Description         | Notes                                            |
| ------------ | ------------ | ------------------- | ------------------------------------------------ |
| `last_name`  | String       | Last name           | Optional                                         |
| `first_name` | String       | First name          | Optional                                         |
| `department` | String       | Department or major | Optional                                         |
| `skills`     | Array/String | List of skills      | Optional, can be array or comma-separated string |
| `photo`      | String       | Photo URL           | Optional                                         |
| `email`      | String       | Email address       | Optional                                         |
| `password`   | String       | Password            | Optional, minimum 8 characters                   |
| `role`       | String       | User role           | Optional, accepts 'user' or 'admin' only         |

**Example**:
```json
{
  "last_name": "Mohamed",
  "first_name": "Ahmed",
  "department": "Software Engineering",
  "skills": ["Python", "Java", "SQL"],
  "photo": "https://example.com/photos/ahmed_new.jpg",
  "email": "ahmed.mohamed@example.com"
}
```

#### Responses
- **200 OK**:
  ```json
  {
    "message": "User updated successfully",
    "user": {
      "id": 123,
      "last_name": "Mohamed",
      "first_name": "Ahmed",
      "email": "ahmed.mohamed@example.com",
      "department": "Software Engineering",
      "skills": ["Python", "Java", "SQL"],
      "photo": "https://example.com/photos/ahmed_new.jpg",
      "role": "user"
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
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only update your own profile"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to update user"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function updateUserProfile(userId, updateData, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updateData),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update profile');
    }
    console.log('Profile updated:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const userId = 123;
const updateData = {
  last_name: 'Mohamed',
  first_name: 'Ahmed',
  department: 'Software Engineering',
  skills: ['Python', 'Java', 'SQL'],
  photo: 'https://example.com/photos/ahmed_new.jpg',
  email: 'ahmed.mohamed@example.com',
};
const jwtToken = 'your_jwt_token_here';

updateUserProfile(userId, updateData, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. Delete User Profile
- **Method**: `DELETE`
- **URL**: `/api/profile/<user_id>`
- **Description**: Delete a user’s profile.
- **Authentication**: Required (JWT, only the profile owner).

#### Path Parameters
| Parameter   | Type    | Description     | Notes            |
| ----------- | ------- | --------------- | ---------------- |
| `user_id` * | Integer | User identifier | Positive integer |

#### Responses
- **200 OK**:
  ```json
  {"message": "User deleted successfully"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid token identity"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only delete your own profile"}
  ```
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to delete user"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function deleteUserProfile(userId, token) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/profile/${userId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete profile');
    }
    console.log('Profile deleted:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const userId = 123;
const jwtToken = 'your_jwt_token_here';

deleteUserProfile(userId, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. Search User Profiles
- **Method**: `GET`
- **URL**: `/api/search`
- **Description**: Search for user profiles based on specified criteria.
- **Authentication**: Required (JWT).

#### Query Parameters
| Parameter         | Type    | Description             | Notes                                  |
| ----------------- | ------- | ----------------------- | -------------------------------------- |
| `name`            | String  | Search by name          | Optional, searches first and last name |
| `department`      | String  | Search by department    | Optional                               |
| `skill`           | String  | Search by skill         | Optional                               |
| `exclude_user_id` | Integer | Exclude a specific user | Optional                               |
| `page`            | Integer | Page number             | Optional, defaults to 1                |
| `per_page`        | Integer | Results per page        | Optional, defaults to 10               |

#### Responses
- **200 OK**:
  ```json
  {
    "results": [
      {
        "id": 124,
        "last_name": "Omar",
        "first_name": "Mohamed",
        "email": "mohamed.omar@example.com",
        "department": "Computer Science",
        "skills": ["Java", "SQL", "Spring"],
        "photo": "https://example.com/photos/mohamed.jpg",
        "role": "user"
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 10
  }
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Missing JWT token"}
  ```

#### JavaScript Example (Frontend):
```javascript
async function searchUsers(searchParams, token) {
  try {
    const query = new URLSearchParams(searchParams).toString();
    const response = await fetch(`https://educonnect-wp9t.onrender.com/api/search?${query}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to search users');
    }
    console.log('Search results:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const searchParams = {
  skill: 'Python',
  department: 'Computer Science',
  page: 1,
  per_page: 20,
};
const jwtToken = 'your_jwt_token_here';

searchUsers(searchParams, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to protect sensitive data.
- Test APIs using tools like Postman or cURL.
- The access token (JWT) must be included in the request header as `Authorization: Bearer <token>` for endpoints requiring authentication.
- Administrative actions (e.g., updating or deleting profiles) are logged using `AuditLogManager` for auditing purposes.
- Skills can be provided as an array or a comma-separated string and will be processed accordingly.
- Users cannot modify or delete other users’ profiles, even if they are admins.