# Authentication APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a local testing environment.

## Overview
The authentication APIs enable user registration, login using sessions, and logout. The system relies on session-based authentication instead of access tokens (JWT) to manage user state.

## Prerequisites
- **Server**: Runs on `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: Not required for user registration and login, but required for protected endpoints (session verification is used).
- **Content Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.
- **Sessions**: Uses sessions to track login state. Browsers must support cookies for session management.

## Endpoints

### 1. # Register a New User

- **Method**: `POST`
- **URL**: `/api/register`
- **Description**: Create a new user account. Supports JSON or form-data requests. Users can provide a profile picture via file upload or a URL.
- **Authentication**: Not required.
- **Content-Type**: `application/json` or `multipart/form-data`

## Request Body

| Field          | Type   | Description                     | Notes                                                                 |
| -------------- | ------ | ------------------------------- | --------------------------------------------------------------------- |
| `first_name` * | String | First name                      | Cannot be empty                                                       |
| `last_name` *  | String | Last name                       | Cannot be empty                                                       |
| `email` *      | String | Email address                   | Must be unique and valid (format: `user@domain.tld`)                  |
| `password` *   | String | Password                        | At least 8 characters                                                 |
| `department` * | String | Department/Specialization       | Cannot be empty                                                       |
| `skills` *     | String | Skills                          | Comma-separated string (e.g., `Python,JavaScript`)                     |
| `photo`        | File   | Profile picture file            | Optional; supported types: PNG, JPG, JPEG (used with `multipart/form-data`) |
| `photo_url`    | String | Profile picture URL             | Optional; must start with `http://` or `https://` (used with `application/json` or `multipart/form-data`) |

**Notes**:
- If both `photo` and `photo_url` are provided, the uploaded `photo` file takes precedence.
- Required fields are marked with an asterisk (*).

**Example (JSON)**:
```json
{
  "first_name": "Ahmed",
  "last_name": "Benali",
  "email": "ahmed.benali@example.com",
  "password": "securepassword123",
  "department": "Computer Science",
  "skills": "Python,JavaScript",
  "photo_url": "https://example.com/photos/ahmed.jpg"
}
```

**Example (Form-data)**:
```
first_name: Ahmed
last_name: Benali
email: ahmed.benali@example.com
password: securepassword123
department: Computer Science
skills: Python,JavaScript
photo: (binary file, e.g., ahmed.jpg)
```

## Responses

- **201 Created**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "first_name": "Ahmed",
      "last_name": "Benali",
      "email": "ahmed.benali@example.com",
      "department": "Computer Science",
      "photo": "https://example.com/static/uploads/ahmed_benali_ahmed.jpg",
      "role": "user"
    }
  }
  ```

- **400 Bad Request** (Missing required fields):
  ```json
  {"error": "Missing required fields"}
  ```

- **400 Bad Request** (Invalid email format):
  ```json
  {"error": "Invalid email format"}
  ```

- **400 Bad Request** (Password too short):
  ```json
  {"error": "Password must be at least 8 characters"}
  ```

- **400 Bad Request** (Email already registered):
  ```json
  {"error": "Email already registered"}
  ```

- **400 Bad Request** (Invalid or unsupported file type for photo):
  ```json
  {"error": "Invalid or unsupported file type"}
  ```

- **400 Bad Request** (Invalid photo URL):
  ```json
  {"error": "Invalid photo URL"}
  ```

- **500 Internal Server Error**:
  ```json
  {"error": "Failed to register user"}
  ```

## Example JavaScript (Frontend)

```javascript
async function registerUser(userData, isFormData = false) {
  try {
    const url = 'https://educonnect-wp9t.onrender.com/api/register';
    let options = {
      method: 'POST',
      credentials: 'include' // Required to send session cookies
    };

    if (isFormData) {
      // For form-data (e.g., with file upload)
      const formData = new FormData();
      for (const key in userData) {
        formData.append(key, userData[key]);
      }
      options.body = formData;
    } else {
      // For JSON
      options.headers = { 'Content-Type': 'application/json' };
      options.body = JSON.stringify(userData);
    }

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }

    console.log('Registration successful:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage with JSON
const userDataJson = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'Computer Science',
  skills: 'Python,JavaScript',
  photo_url: 'https://example.com/photos/ahmed.jpg'
};

registerUser(userDataJson)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// Usage with Form-data (e.g., with file upload)
const userDataForm = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'Computer Science',
  skills: 'Python,JavaScript',
  photo: document.querySelector('input[type="file"]').files[0] // Example file input
};

registerUser(userDataForm, true)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Login
- **Method**: `POST`
- **URL**: `/api/login`
- **Description**: Log in a user and create a session.
- **Authentication**: Not required.

#### Request Body
| Field        | Type   | Description             | Notes                  |
| ------------ | ------ | ----------------------- | ---------------------- |
| `email` *    | String | Email address           | Cannot be empty        |
| `password` * | String | Password                | Cannot be empty        |

**Example**:
```json
{
  "email": "ahmed.benali@example.com",
  "password": "securepassword123"
}
```

#### Responses
- **200 OK**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "email": "ahmed.benali@example.com",
      "role": "user"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Email and password are required"}
  ```
- **401 Unauthorized**:
  ```json
  {"error": "Invalid email or password"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function loginUser(credentials) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
      credentials: 'include' // Required to send session cookies
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    console.log('Login successful:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const credentials = {
  email: 'ahmed.benali@example.com',
  password: 'securepassword123'
};

loginUser(credentials)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. Logout
- **Method**: `POST`
- **URL**: `/api/logout`
- **Description**: Terminate the current user session.
- **Authentication**: Not required (but the session will be terminated if it exists).

#### Request Body
No body required.

#### Responses
- **200 OK**:
  ```json
  {"message": "Logged out successfully"}
  ```

#### Example JavaScript (Frontend):
```javascript
async function logoutUser() {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/logout', {
      method: 'POST',
      credentials: 'include' // Required to send session cookies
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Logout failed');
    }
    console.log('Logout successful:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
logoutUser()
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to secure sensitive data.
- Test the APIs using tools like Postman or cURL.
- Cookies must be enabled in the browser to support session management.
- For endpoints requiring authentication, an active session (containing `user_id` and `role`) is verified.
- To enhance security, ensure session cookies are sent with the `HttpOnly` and `Secure` attributes in production.
- Session duration depends on the server's `PERMANENT_SESSION_LIFETIME` configuration.