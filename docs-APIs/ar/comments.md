# وثائق واجهات برمجة التطبيقات للتعليقات (Comments APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الخاصة بالتعليقات أدوات لإدارة التعليقات على المنشورات، بما في ذلك إضافة تعليقات جديدة، استرجاع التعليقات، تحديث التعليقات، وحذفها. تتطلب معظم نقاط النهاية جلسة مستخدم نشطة للمصادقة.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة (مع `user_id` في الجلسة) للوصول إلى نقاط النهاية التي تتطلب المصادقة، باستثناء استرجاع التعليقات.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. إضافة تعليق
- **الطريقة**: `POST`
- **الرابط**: `/posts/<post_id>/comments`
- **الوصف**: إضافة تعليق جديد إلى منشور محدد.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### جسم الطلب
| الحقل          | النوع           | الوصف              | ملاحظات                                     |
| -------------- | --------------- | ------------------ | ------------------------------------------- |
| `content` *    | String          | محتوى التعليق      | لا يمكن أن يكون فارغًا، الحد الأقصى 1000 حرف |
| `created_at` * | String/Datetime | تاريخ ووقت الإنشاء | تنسيق ISO أو كائن datetime                  |

**ملاحظة**: حقل `user_id` غير مسموح به في جسم الطلب، حيث يتم استرجاعه تلقائيًا من الجلسة.

**مثال**:
```json
{
  "content": "Great project, looking forward to more updates!",
  "created_at": "2025-05-22T07:28:00Z"
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const commentData = {
  content: 'Great project, looking forward to more updates!',
  created_at: '2025-05-22T07:28:00Z'
};

addComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع تعليقات منشور
- **الطريقة**: `GET`
- **الرابط**: `/posts/<post_id>/comments`
- **الوصف**: استرجاع قائمة تعليقات مُصفحة لمنشور محدد.
- **المصادقة**: غير مطلوبة.

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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getComments(1, 1, 20)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. تحديث تعليق
- **الطريقة**: `PUT`
- **الرابط**: `/comments/<comment_id>`
- **الوصف**: تحديث محتوى تعليق موجود.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### جسم الطلب
| الحقل       | النوع  | الوصف                | ملاحظات               |
| ----------- | ------ | -------------------- | --------------------- |
| `content` * | String | محتوى التعليق الجديد | لا يمكن أن يكون فارغًا |

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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const commentData = {
  content: 'Updated comment content'
};

updateComment(1, commentData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. حذف تعليق
- **الطريقة**: `DELETE`
- **الرابط**: `/comments/<comment_id>`
- **الوصف**: حذف تعليق بناءً على المعرف.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deleteComment(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة تحتوي على `user_id`.
- يتم تسجيل الإجراءات المتعلقة بتحديث أو حذف التعليقات باستخدام `AuditLogManager` لأغراض التدقيق.
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.
- يتم التحقق من أن محتوى التعليق يتراوح بين 1 و1000 حرف، ويتم رفض حقل `user_id` في جسم الطلب لأن المستخدم يتم تحديده من الجلسة.