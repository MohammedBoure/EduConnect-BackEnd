# وثائق واجهات برمجة التطبيقات للمصادقة (Authentication APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
تتيح واجهات المصادقة تسجيل المستخدمين الجدد، تسجيل الدخول باستخدام الجلسات، وتسجيل الخروج. يتم الاعتماد على الجلسات بدلاً من رموز الوصول (JWT) لإدارة حالة المستخدم.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: غير مطلوبة لتسجيل المستخدمين وتسجيل الدخول، ولكنها مطلوبة للواجهات المحمية (يتم التحقق من الجلسة).
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. تسجيل مستخدم جديد
- **الطريقة**: `POST`
- **الرابط**: `/api/register`
- **الوصف**: إنشاء حساب مستخدم جديد.
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل          | النوع  | الوصف                  | ملاحظات                  |
| -------------- | ------ | ---------------------- | ------------------------ |
| `first_name` * | String | الاسم الأول            | لا يمكن أن يكون فارغًا    |
| `last_name` *  | String | الاسم الأخير           | لا يمكن أن يكون فارغًا    |
| `email` *      | String | البريد الإلكتروني      | يجب أن يكون فريدًا وصالحًا |
| `password` *   | String | كلمة المرور            | لا تقل عن 8 أحرف         |
| `department` * | String | القسم/التخصص           | لا يمكن أن يكون فارغًا    |
| `skills` *     | String | المهارات               | مفصولة بفواصل أو كقائمة  |
| `photo`        | String | رابط صورة الملف الشخصي | اختياري                  |

**مثال**:
```json
{
  "first_name": "Ahmed",
  "last_name": "Benali",
  "email": "ahmed.benali@example.com",
  "password": "securepassword123",
  "department": "Computer Science",
  "skills": "Python, JavaScript",
  "photo": "https://example.com/photos/ahmed.jpg"
}
```

#### الاستجابات
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
      "photo": "https://example.com/photos/ahmed.jpg",
      "role": "user"
    }
  }
  ```
- **400 Bad Request**:
  ```json
  {"error": "Missing required fields"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Invalid email format"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Password must be at least 8 characters"}
  ```
- **400 Bad Request**:
  ```json
  {"error": "Email already registered"}
  ```
- **500 Internal Server Error**:
  ```json
  {"error": "Failed to register user"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function registerUser(userData) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
      credentials: 'include' // ضروري لإرسال ملفات تعريف الارتباط للجلسة
    });

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

// استخدام الدالة
const userData = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'Computer Science',
  skills: 'Python, JavaScript',
  photo: 'https://example.com/photos/ahmed.jpg'
};

registerUser(userData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. تسجيل الدخول
- **الطريقة**: `POST`
- **الرابط**: `/api/login`
- **الوصف**: تسجيل دخول المستخدم وإنشاء جلسة.
- **المصادقة**: غير مطلوبة.

#### جسم الطلب
| الحقل        | النوع  | الوصف             | ملاحظات               |
| ------------ | ------ | ----------------- | --------------------- |
| `email` *    | String | البريد الإلكتروني | لا يمكن أن يكون فارغًا |
| `password` * | String | كلمة المرور       | لا يمكن أن يكون فارغًا |

**مثال**:
```json
{
  "email": "ahmed.benali@example.com",
  "password": "securepassword123"
}
```

#### الاستجابات
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

#### مثال JavaScript (Frontend):
```javascript
async function loginUser(credentials) {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
      credentials: 'include' // ضروري لإرسال ملفات تعريف الارتباط للجلسة
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

// استخدام الدالة
const credentials = {
  email: 'ahmed.benali@example.com',
  password: 'securepassword123'
};

loginUser(credentials)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 3. تسجيل الخروج
- **الطريقة**: `POST`
- **الرابط**: `/api/logout`
- **الوصف**: إنهاء جلسة المستخدم الحالية.
- **المصادقة**: غير مطلوبة (لكن الجلسة سيتم إنهاؤها إذا كانت موجودة).

#### جسم الطلب
لا يتطلب جسمًا.

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "Logged out successfully"}
  ```

#### مثال JavaScript (Frontend):
```javascript
async function logoutUser() {
  try {
    const response = await fetch('https://educonnect-wp9t.onrender.com/api/logout', {
      method: 'POST',
      credentials: 'include' // ضروري لإرسال ملفات تعريف الارتباط للجلسة
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

// استخدام الدالة
logoutUser()
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة (تحتوي على `user_id` و`role`).
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.