# وثائق واجهات برمجة التطبيقات للمنشورات (Posts APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الخاصة بالمنشورات أدوات لإدارة المنشورات، بما في ذلك إنشاء منشورات جديدة، استرجاع المنشورات (للمستخدمين أو الإداريين أو جميع المنشورات)، تحديث المنشورات، وحذفها. بعض نقاط النهاية تتطلب جلسة مستخدم نشطة للمصادقة، بينما البعض الآخر متاح للجميع.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة (مع `user_id` في الجلسة) للوصول إلى نقاط النهاية التي تتطلب المصادقة (مثل إنشاء، تحديث، أو حذف المنشورات).
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. إنشاء منشور
- **الطريقة**: `POST`
- **الرابط**: `/posts`
- **الوصف**: إنشاء منشور جديد للمستخدم المصادق عليه مع صورة اختيارية (إما كملف مرفوع أو رابط URL).
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة عبر `login_required`).

### الطلب
- **نوع المحتوى**: 
  - `application/json` للبيانات بصيغة JSON.
  - `multipart/form-data` لرفع الملفات مع حقول النموذج.
- **الجسم**:
  | الحقل       | النوع  | الوصف                           | ملاحظات                              |
  |-------------|--------|---------------------------------|--------------------------------------|
  | `title` *   | نص     | عنوان المنشور                  | مطلوب، لا يمكن أن يكون فارغًا أو يحتوي على مسافات فقط |
  | `content` * | نص     | محتوى المنشور                  | مطلوب، لا يمكن أن يكون فارغًا أو يحتوي على مسافات فقط |
  | `image`     | ملف    | ملف الصورة                      | اختياري، يجب أن يكون نوع ملف مدعوم (مثل `.jpg`، `.png`) إذا تم توفيره |
  | `image_url` | نص     | رابط الصورة                     | اختياري، يجب أن يبدأ بـ `http://` أو `https://` إذا تم توفيره |

  **ملاحظات**:
  - إذا تم توفير كل من `image` (ملف) و`image_url`، يتم تفضيل الملف المرفوع.
  - أنواع الملفات المدعومة لـ `image` يتم تحديدها من قبل الخادم (مثل `.jpg`، `.png`، `.gif`).

**مثال (JSON)**:
```json
{
  "title": "إعلان مشروع جديد",
  "content": "نحن متحمسون للإعلان عن مشروع جديد...",
  "image_url": "https://example.com/images/project.jpg"
}
```

**مثال (Form-Data)**:
```
title: إعلان مشروع جديد
content: نحن متحمسون للإعلان عن مشروع جديد...
image: (ملف ثنائي، مثل project.jpg)
```

### الردود
- **201 تم الإنشاء**:
  ```json
  {
    "message": "تم إنشاء المنشور بنجاح",
    "post": {
      "id": 1,
      "title": "إعلان مشروع جديد",
      "content": "نحن متحمسون للإعلان عن مشروع جديد...",
      "image": "https://educonnect-wp9t.onrender.com/static/uploads_posts/1_1697051234.567_project.jpg",
      "created_at": "2025-05-22T07:28:00Z",
      "user_id": 1,
      "author": {
        "first_name": "أحمد",
        "last_name": "بنعلي",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 طلب غير صالح** (بيانات طلب غير صالحة):
  ```json
  {"error": "بيانات الطلب غير صالحة"}
  ```
- **400 طلب غير صالح** (عنوان أو محتوى فارغ):
  ```json
  {"error": "العنوان والمحتوى لا يمكن أن يكونا فارغين"}
  ```
- **400 طلب غير صالح** (نوع ملف غير صالح):
  ```json
  {"error": "نوع ملف غير صالح أو غير مدعوم للصورة"}
  ```
- **400 طلب غير صالح** (رابط صورة غير صالح):
  ```json
  {"error": "رابط الصورة غير صالح"}
  ```
- **401 غير مصرح**:
  ```json
  {"error": "غير مصرح: لا توجد جلسة نشطة"}
  ```
- **500 خطأ داخلي في الخادم**:
  ```json
  {"error": "فشل في إنشاء المنشور"}
  ```

### مثال JavaScript (واجهة المستخدم)
```javascript
async function createPost(postData, imageFile = null) {
  try {
    const formData = new FormData();
    formData.append('title', postData.title);
    formData.append('content', postData.content);
    if (imageFile) {
      formData.append('image', imageFile);
    } else if (postData.image_url) {
      formData.append('image_url', postData.image_url);
    }

    const response = await fetch('https://educonnect-wp9t.onrender.com/posts', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'فشل في إنشاء المنشور');
    }
    console.log('تم إنشاء المنشور بنجاح:', data);
    return data;
  } catch (error) {
    console.error('خطأ:', error.message);
    throw error;
  }
}

// الاستخدام
const postData = {
  title: 'إعلان مشروع جديد',
  content: 'نحن متحمسون للإعلان عن مشروع جديد...',
  image_url: 'https://example.com/images/project.jpg'
};

// مثال برابط صورة
createPost(postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// مثال بملف صورة
const imageFile = document.querySelector('#imageInput').files[0];
createPost({ title: postData.title, content: postData.content }, imageFile)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع منشور معين
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/posts/<post_id>`
- **الوصف**: استرجاع منشور واحد بناءً على المعرف (متاح للجميع).
- **المصادقة**: غير مطلوبة.

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getPost(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. استرجاع منشورات مستخدم
- **الطريقة**: `GET`
- **الرابط**: `/posts/user/<user_id>`
- **الوصف**: استرجاع قائمة منشورات مُصفحة لمستخدم محدد (متاح للجميع).
- **المصادقة**: غير مطلوبة.

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
- **404 Not Found**:
  ```json
  {"error": "User not found"}
  ```

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getUserPosts(1, 1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. استرجاع منشورات الإداريين
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/posts/admin_user_posts`
- **الوصف**: استرجاع قائمة منشورات مُصفحة للمستخدمين الذين لديهم دور الإدارة (متاح للجميع).
- **المصادقة**: غير مطلوبة.

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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getAdminUserPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 5. استرجاع منشورات جميع المستخدمين
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/posts/users_posts`
- **الوصف**: استرجاع قائمة منشورات مُصفحة لجميع المستخدمين (متاح للجميع).
- **المصادقة**: غير مطلوبة.

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

// استخدام الدالة
getAllUsersPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 6. استرجاع جميع المنشورات
- **الطريقة**: `GET`, `OPTIONS`
- **الرابط**: `/posts`
- **الوصف**: استرجاع قائمة مُصفحة لجميع المنشورات (متاح للجميع).
- **المصادقة**: غير مطلوبة.

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
    "total": 100,
    "page": 1,
    "pages": 10,
    "per_page": 10
  }
  ```

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getAllPosts(1, 10)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 7. تحديث منشور
- **الطريقة**: `PUT`
- **الرابط**: `/posts/<post_id>`
- **الوصف**: تحديث منشور موجود (لصاحب المنشور أو المسؤولين فقط).
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة عبر `login_required`).

### الطلب
- **نوع المحتوى**: 
  - `application/json` للبيانات بصيغة JSON.
  - `multipart/form-data` لرفع الملفات مع حقول النموذج.
- **الجسم**:
  | الحقل       | النوع  | الوصف                           | ملاحظات                              |
  |-------------|--------|---------------------------------|--------------------------------------|
  | `title` *   | نص     | عنوان المنشور                  | مطلوب، لا يمكن أن يكون فارغًا أو يحتوي على مسافات فقط |
  | `content` * | نص     | محتوى المنشور                  | مطلوب، لا يمكن أن يكون فارغًا أو يحتوي على مسافات فقط |
  | `image`     | ملف    | ملف الصورة                      | اختياري، يجب أن يكون نوع ملف مدعوم (مثل `.jpg`، `.png`) إذا تم توفيره |
  | `image_url` | نص     | رابط الصورة                     | اختياري، يجب أن يبدأ بـ `http://` أو `https://` إذا تم توفيره، أو فارغ لإزالة الصورة |

  **ملاحظات**:
  - إذا تم توفير كل من `image` (ملف) و`image_url`، يتم تفضيل الملف المرفوع.
  - إذا لم يتم توفير صورة جديدة، يتم الاحتفاظ بالصورة الحالية.
  - إرسال `image_url` فارغ (`""`) يزيل الصورة الموجودة.
  - أنواع الملفات المدعومة لـ `image` يتم تحديدها من قبل الخادم (مثل `.jpg`، `.png`، `.gif`).

**مثال (JSON)**:
```json
{
  "title": "إعلان مشروع محدث",
  "content": "محتوى محدث لإعلان المشروع...",
  "image_url": "https://example.com/images/updated_project.jpg"
}
```

**مثال (Form-Data)**:
```
title: إعلان مشروع محدث
content: محتوى محدث لإعلان المشروع...
image: (ملف ثنائي، مثل updated_project.jpg)
```

### الردود
- **200 نجاح**:
  ```json
  {
    "message": "تم تحديث المنشور بنجاح",
    "post": {
      "id": 1,
      "title": "إعلان مشروع محدث",
      "content": "محتوى محدث لإعلان المشروع...",
      "image": "https://educonnect-wp9t.onrender.com/static/uploads_posts/1_1697051234.567_updated_project.jpg",
      "created_at": "2025-05-22T07:28:00Z",
      "user_id": 1,
      "author": {
        "first_name": "أحمد",
        "last_name": "بنعلي",
        "photo": "https://example.com/photos/ahmed.jpg"
      }
    }
  }
  ```
- **400 طلب غير صالح** (بيانات طلب غير صالحة):
  ```json
  {"error": "بيانات الطلب غير صالحة"}
  ```
- **400 طلب غير صالح** (عنوان أو محتوى فارغ):
  ```json
  {"error": "العنوان والمحتوى لا يمكن أن يكونا فارغين"}
  ```
- **400 طلب غير صالح** (نوع ملف غير صالح):
  ```json
  {"error": "نوع ملف غير صالح أو غير مدعوم للصورة"}
  ```
- **400 طلب غير صالح** (رابط صورة غير صالح):
  ```json
  {"error": "رابط الصورة غير صالح"}
  ```
- **401 غير مصرح**:
  ```json
  {"error": "غير مصرح: لا توجد جلسة نشطة"}
  ```
- **403 ممنوع**:
  ```json
  {"error": "ممنوع: يمكنك تحديث منشوراتك فقط"}
  ```
- **404 غير موجود**:
  ```json
  {"error": "المنشور غير موجود"}
  ```
- **500 خطأ داخلي في الخادم**:
  ```json
  {"error": "فشل في تحديث المنشور"}
  ```

### مثال JavaScript (واجهة المستخدم)
```javascript
async function updatePost(postId, postData, imageFile = null) {
  try {
    const formData = new FormData();
    formData.append('title', postData.title);
    formData.append('content', postData.content);
    if (imageFile) {
      formData.append('image', imageFile);
    } else if (postData.image_url !== undefined) {
      formData.append('image_url', postData.image_url);
    }

    const response = await fetch(`https://educonnect-wp9t.onrender.com/posts/${postId}`, {
      method: 'PUT',
      body: formData,
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'فشل في تحديث المنشور');
    }
    console.log('تم تحديث المنشور بنجاح:', data);
    return data;
  } catch (error) {
    console.error('خطأ:', error.message);
    throw error;
  }
}

// الاستخدام
const postData = {
  title: 'إعلان مشروع محدث',
  content: 'محتوى محدث لإعلان المشروع...',
  image_url: 'https://example.com/images/updated_project.jpg'
};

// مثال برابط صورة
updatePost(1, postData)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// مثال بملف صورة
const imageFile = document.querySelector('#imageInput').files[0];
updatePost(1, { title: postData.title, content: postData.content }, imageFile)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// مثال لإزالة الصورة
updatePost(1, { title: postData.title, content: postData.content, image_url: '' })
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 8. حذف منشور
- **الطريقة**: `DELETE`
- **الرابط**: `/posts/<post_id>`
- **الوصف**: حذف منشور بناءً على المعرف (للإداريين فقط).
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### الاستجابات
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
deletePost(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة تحتوي على `user_id`.
- يتم تسجيل الإجراءات المتعلقة بإنشاء، تحديث، وحذف المنشورات باستخدام `AuditLogManager` لأغراض التدقيق.
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.
- نقطة النهاية `/posts/<post_id>` (GET) مكررة في الكود (`get_post` و`get_post_by_id`). تم توثيقها مرة واحدة كونها متاحة للجميع وتعيد نفس البيانات.
- تحديث المنشورات مقيد بصاحب المنشور أو المستخدمين بدور `admin`.
- حذف المنشورات متاح فقط للإداريين، كما هو موضح في وصف نقطة النهاية.