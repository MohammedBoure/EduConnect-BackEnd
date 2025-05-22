# Messages APIs Documentation

## Server URL
`https://educonnect-wp9t.onrender.com`  
Replace with `http://127.0.0.1:5000` if working in a local testing environment.

## Overview
The Messages APIs provide functionality for sending messages between users and retrieving messages between two users. All endpoints require an active user session for authentication.

## Prerequisites
- **Server**: Runs on `https://educonnect-wp9t.onrender.com` in production.
- **Authentication**: Requires an active user session (with `user_id` in the session) to access endpoints.
- **Content Type**: `application/json` for requests with a body.
- **HTTPS**: Recommended in production to secure sensitive data.
- **Sessions**: Uses sessions to track login state. Browsers must support cookies for session management.

## Endpoints

### 1. Send a Message
- **Method**: `POST`
- **URL**: `/messages`
- **Description**: Send a new message from the current user to another user.
- **Authentication**: Required (active user session).

#### Request Body
| Field           | Type    | Description           | Notes                  |
| --------------- | ------- | --------------------- | ---------------------- |
| `receiver_id` * | Integer | Recipient's user ID   | Required               |
| `content` *     | String  | Message content       | Cannot be empty        |

**Example**:
```json
{
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
  {"error": "Receiver ID and non-empty content are required."}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid receiver_id format"}
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
    const response = await fetch('https://educonnect-wp9t.onrender.com/messages', {
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
  receiver_id: 2,
  content: "Hello, how's the project going?"
};

sendMessage(messageData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. Retrieve Messages Between Users
- **Method**: `GET`
- **URL**: `/messages/<other_user_id>`
- **Description**: Retrieve paginated messages between the current user and another user.
- **Authentication**: Required (active user session).

#### Query Parameters
| Parameter   | Type    | Description                  | Default |
| ----------- | ------- | ---------------------------- | ------- |
| `page`      | Integer | Page number                  | 1       |
| `per_page`  | Integer | Number of messages per page  | 30      |

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

#### Example JavaScript (Frontend):
```javascript
async function getMessages(otherUserId, page = 1, perPage = 30) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/messages/${otherUserId}?page=${page}&per_page=${perPage}`, {
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
getMessages(2, 1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## General Notes
- HTTPS is recommended in production to secure sensitive data.
- Test the APIs using tools like Postman or cURL.
- Cookies must be enabled in the browser to support session management.
- For endpoints requiring authentication, an active session containing `user_id` is verified.
- Actions related to sending messages are logged using `AuditLogManager` for auditing purposes.
- To enhance security, ensure session cookies are sent with the `HttpOnly` and `Secure` attributes in production.
- Session duration depends on the server's `PERMANENT_SESSION_LIFETIME` configuration.
- Sending messages to oneself (same sender and receiver) is prohibited.