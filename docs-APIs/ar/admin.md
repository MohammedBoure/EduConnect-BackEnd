# وثائق واجهات برمجة التطبيقات الإدارية (Admin APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الإدارية أدوات لإدارة المستخدمين، المنشورات، التعليقات، والرسائل. هذه الواجهات مخصصة للمستخدمين بصلاحيات الإدارة (دور `admin`)، وتتطلب جلسة نشطة للوصول إلى معظم نقاط النهاية.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة مع دور `admin` للوصول إلى معظم نقاط النهاية، باستثناء طلبات `OPTIONS`.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات部分

System: ### وثائق واجهات برمجة التطبيقات الإدارية (Admin APIs)

<xaiArtifact artifact_id="5c3dff7c-7160-45a1-b385-25b4c67ff7ef" artifact_version_id="841ee966-67c2-41ff-9136-2e0072222d1f" title="Admin APIs Documentation" contentType="text/markdown">

# وثائق واجهات برمجة التطبيقات الإدارية (Admin APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الإدارية أدوات لإدارة المستخدمين، المنشورات، التعليقات، والرسائل. هذه الواجهات مخصصة للمستخدمين بصلاحيات الإدارة (دور `admin`)، وتتطلب جلسة نشطة للوصول إلى معظم نقاط النهاية.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة مع دور `admin` للوصول إلى معظم نقاط النهاية، باستثناء طلبات `OPTIONS`.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. استرجاع قائمة المستخدمين
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/admin/users`
- **الوصف**: استرجاع قائمة مستخدمين مُصفحة.
- **المصادقة**: غير مطلوبة لطلبات `OPTIONS`، مطلوبة (دور `admin`) لطلبات `GET`.

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                   | افتراضي |
| ---------- | ------- | ----------------------- | ------- |
| `page`     | Integer | رقم الصفحة              | 1       |
| `per_page` | Integer | عدد المستخدمين لكل صفحة | 10      |

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
listUsers(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع ملف المستخدم
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/admin/users/<user_id>`
- **الوصف**: استرجاع تفاصيل مستخدم محدد بناءً على المعرف.
- **المصادقة**: غير مطلوبة لطلبات `OPTIONS`، مطلوبة (دور `admin`) لطلبات `GET`.

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getUserProfile(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. تحديث ملف المستخدم
- **الطريقة**: `PUT`
- **الرابط**: `/admin/users/<user_id>`
- **الوصف**: تحديث تفاصيل مستخدم، بما في ذلك الدور.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل        | النوع        | الوصف                  | ملاحظات                         |
| ------------ | ------------ | ---------------------- | ------------------------------- |
| `first_name` | String       | الاسم الأول            | اختياري                         |
| `last_name`  | String       | الاسم الأخير           | اختياري                         |
| `email`      | String       | البريد الإلكتروني      | اختياري، يجب أن يكون صالحًا      |
| `password`   | String       | كلمة المرور            | اختياري، لا تقل عن 8 أحرف       |
| `department` | String       | القسم/التخصص           | اختياري                         |
| `skills`     | String/Array | المهارات               | اختياري، مفصولة بفواصل أو قائمة |
| `photo`      | String       | رابط صورة الملف الشخصي | اختياري                         |
| `role`       | String       | دور المستخدم           | اختياري، `user` أو `admin`      |

**مثال**:
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

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
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

### 4. حذف مستخدم
- **الطريقة**: `DELETE`
- **الرابط**: `/admin/users/<user_id>`
- **الوصف**: حذف مستخدم بناءً على المعرف.
- **المصادقة**: مطلوبة (دور `admin`).

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deleteUser(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 5. إنشاء منشور
- **الطريقة**: `POST`
- **الرابط**: `/admin/posts/create`
- **الوصف**: إنشاء منشور جديد نيابة عن مستخدم.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل       | النوع   | الوصف                | ملاحظات               |
| ----------- | ------- | -------------------- | --------------------- |
| `user_id` * | Integer | معرف المستخدم المنشئ | مطلوب                 |
| `title` *   | String  | عنوان المنشور        | لا يمكن أن يكون فارغًا |
| `content` * | String  | محتوى المنشور        | لا يمكن أن يكون فارغًا |
| `image`     | String  | رابط الصورة          | اختياري               |

**مثال**:
```json
{
  "user_id": 1,
  "title": "New Project Announcement",
  "content": "We are excited to announce a new project...",
  "image": "https://example.com/images/project.jpg"
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
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

### 6. استرجاع قائمة المنشورات
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/admin/posts`
- **الوصف**: استرجاع قائمة منشورات مُصفحة.
- **المصادقة**: غير مطلوبة لطلبات `OPTIONS`، مطلوبة (دور `admin`) لطلبات `GET`.

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                  | افتراضي |
| ---------- | ------- | ---------------------- | ------- |
| `page`     | Integer | رقم الصفحة             | 1       |
| `per_page` | Integer | عدد المنشورات لكل صفحة | 10      |

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
listPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 7. تحديث منشور
- **الطريقة**: `PUT`
- **الرابط**: `/admin/posts/<post_id>`
- **الوصف**: تحديث منشور موجود.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل     | النوع  | الوصف         | ملاحظات                                      |
| --------- | ------ | ------------- | -------------------------------------------- |
| `title`   | String | عنوان المنشور | اختياري، لا يمكن أن يكون فارغًا إذا تم توفيره |
| `content` | String | محتوى المنشور | اختياري، لا يمكن أن يكون فارغًا إذا تم توفيره |
| `image`   | String | رابط الصورة   | اختياري                                      |

**مثال**:
```json
{
  "title": "Updated Project Announcement",
  "content": "Updated content for the project announcement...",
  "image": "https://example.com/images/updated_project.jpg"
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const postData = {
  title: 'Updated Project Announcement',
  content: 'Updated content for the project announcement...',
  image: 'https://example.com/images/updated_project.jpg'
};

updatePost(1, postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 8. حذف منشور
- **الطريقة**: `DELETE`
- **الرابط**: `/admin/posts/<post_id>`
- **الوصف**: حذف منشور بناءً على المعرف.
- **المصادقة**: مطلوبة (دور `admin`).

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deletePost(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 9. إضافة تعليق
- **الطريقة**: `POST`
- **الرابط**: `/admin/posts/<post_id>/comments`
- **الوصف**: إضافة تعليق إلى منشور.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل          | النوع           | الوصف                   | ملاحظات                    |
| -------------- | --------------- | ----------------------- | -------------------------- |
| `content` *    | String          | محتوى التعليق           | لا يمكن أن يكون فارغًا      |
| `created_at` * | String/Datetime | تاريخ ووقت الإنشاء      | تنسيق ISO أو كائن datetime |
| `user_id` *    | Integer         | معرف المستخدم الذي يعلق | مطلوب                      |

**مثال**:
```json
{
  "content": "Great project, looking forward to more updates!",
  "created_at": "2025-05-22T07:28:00Z",
  "user_id": 1
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const commentData = {
  content: 'Great project, looking forward to more updates!',
  created_at: '2025-05-22T07:28:00Z',
  user_id: 1
};

addComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 10. استرجاع قائمة التعليقات
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/admin/comments`
- **الوصف**: استرجاع قائمة تعليقات مُصفحة.
- **المصادقة**: غير مطلوبة لطلبات `OPTIONS`، مطلوبة (دور `admin`) لطلبات `GET`.

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                  | افتراضي |
| ---------- | ------- | ---------------------- | ------- |
| `page`     | Integer | رقم الصفحة             | 1       |
| `per_page` | Integer | عدد التعليقات لكل صفحة | 20      |

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
listComments(1, 20)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 11. تحديث تعليق
- **الطريقة**: `PUT`
- **الرابط**: `/admin/comments/<comment_id>`
- **الوصف**: تحديث تعليق موجود.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل       | النوع  | الوصف         | ملاحظات               |
| ----------- | ------ | ------------- | --------------------- |
| `content` * | String | محتوى التعليق | لا يمكن أن يكون فارغًا |

**مثال**:
```json
{
  "content": "Updated comment content"
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const commentData = {
  content: 'Updated comment content'
};

updateComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 12. حذف تعليق
- **الطريقة**: `DELETE`, `OPTIONS`
- **الرابط**: `/admin/comments/<comment_id>`
- **الوصف**: حذف تعليق بناءً على المعرف.
- **المصادقة**: مطلوبة (دور `admin`) لطلبات `DELETE`.

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deleteComment(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 13. استرجاع قائمة الرسائل
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/admin/messages`
- **الوصف**: استرجاع قائمة رسائل مُصفحة.
- **المصادقة**: غير مطلوبة لطلبات `OPTIONS`، مطلوبة (دور `admin`) لطلبات `GET`.

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                | افتراضي |
| ---------- | ------- | -------------------- | ------- |
| `page`     | Integer | رقم الصفحة           | 1       |
| `per_page` | Integer | عدد الرسائل لكل صفحة | 30      |

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
listMessages(1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 14. إرسال رسالة
- **الطريقة**: `POST`
- **الرابط**: `/admin/messages`
- **الوصف**: إرسال رسالة جديدة من مستخدم إلى آخر.
- **المصادقة**: مطلوبة (دور `admin`).

#### جسم الطلب
| الحقل           | النوع   | الوصف         | ملاحظات               |
| --------------- | ------- | ------------- | --------------------- |
| `sender_id` *   | Integer | معرف المرسل   | مطلوب                 |
| `receiver_id` * | Integer | معرف المستلم  | مطلوب                 |
| `content` *     | String  | محتوى الرسالة | لا يمكن أن يكون فارغًا |

**مثال**:
```json
{
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Hello, how's the project going?"
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const messageData = {
  sender_id: 1,
  receiver_id: 2,
  content: "Hello, how's the project going?"
};

sendMessage(messageData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 15. حذف رسالة
- **الطريقة**: `DELETE`
- **الرابط**: `/admin/messages/<message_id>`
- **الوصف**: حذف رسالة بناءً على المعرف.
- **المصادقة**: مطلوبة (دور `admin`).

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deleteMessage(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 16. استرجاع الرسائل بين مستخدمين
- **الطريقة**: `GET`
- **الرابط**: `/admin/messages/<current_user_id>/<other_user_id>`
- **الوصف**: استرجاع الرسائل بين مستخدمين اثنين، مُصفحة.
- **المصادقة**: مطلوبة (دور `admin`).

#### معلمات الاستعلام
| المعلمة    | النوع   | الوصف                | افتراضي |
| ---------- | ------- | -------------------- | ------- |
| `page`     | Integer | رقم الصفحة           | 1       |
| `per_page` | Integer | عدد الرسائل لكل صفحة | 30      |

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getMessages(1, 2, 1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة تحتوي على `user_id` و`role` بقيمة `admin`.
- يتم تسجيل جميع الإجراءات الإدارية (مثل تحديث أو حذف المستخدمين، المنشورات، التعليقات، أو الرسائل) باستخدام `AuditLogManager` لأغراض التدقيق.
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.