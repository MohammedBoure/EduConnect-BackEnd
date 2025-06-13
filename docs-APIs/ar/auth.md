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

### 1. # تسجيل مستخدم جديد

- **الطريقة**: `POST`
- **الرابط**: `/api/register`
- **الوصف**: إنشاء حساب مستخدم جديد. يدعم طلبات JSON أو form-data. يمكن للمستخدمين تقديم صورة شخصية عبر رفع ملف أو رابط URL.
- **المصادقة**: غير مطلوبة.
- **نوع المحتوى**: `application/json` أو `multipart/form-data`

## جسم الطلب

| الحقل          | النوع  | الوصف                           | ملاحظات                                                               |
| -------------- | ------ | ------------------------------- | --------------------------------------------------------------------- |
| `first_name` * | نص     | الاسم الأول                    | لا يمكن أن يكون فارغًا                                                |
| `last_name` *  | نص     | الاسم الأخير                   | لا يمكن أن يكون فارغًا                                                |
| `email` *      | نص     | البريد الإلكتروني              | يجب أن يكون فريدًا وصالحًا (الصيغة: `user@domain.tld`)              |
| `password` *   | نص     | كلمة المرور                    | يجب أن تكون 8 أحرف على الأقل                                         |
| `department` * | نص     | القسم/التخصص                   | لا يمكن أن يكون فارغًا                                                |
| `skills` *     | نص     | المهارات                       | سلسلة مفصولة بفواصل (مثال: `Python,JavaScript`)                     |
| `photo`        | ملف    | ملف الصورة الشخصية             | اختياري؛ الأنواع المدعومة: PNG، JPG، JPEG (يُستخدم مع `multipart/form-data`) |
| `photo_url`    | نص     | رابط الصورة الشخصية            | اختياري؛ يجب أن يبدأ بـ `http://` أو `https://` (يُستخدم مع `application/json` أو `multipart/form-data`) |

**ملاحظات**:
- إذا تم تقديم كل من `photo` و `photo_url`، يتم الأولوية لملف `photo` المرفوع.
- الحقول المطلوبة موسومة بعلامة النجمة (*).

**مثال (JSON)**:
```json
{
  "first_name": "أحمد",
  "last_name": "بنعلي",
  "email": "ahmed.benali@example.com",
  "password": "securepassword123",
  "department": "علوم الحاسوب",
  "skills": "Python,JavaScript",
  "photo_url": "https://example.com/photos/ahmed.jpg"
}
```

**مثال (Form-data)**:
```
first_name: أحمد
last_name: بنعلي
email: ahmed.benali@example.com
password: securepassword123
department: علوم الحاسوب
skills: Python,JavaScript
photo: (ملف ثنائي، مثال: ahmed.jpg)
```

## الردود

- **201 تم الإنشاء**:
  ```json
  {
    "message": "تم تسجيل المستخدم بنجاح",
    "user": {
      "id": 1,
      "first_name": "أحمد",
      "last_name": "بنعلي",
      "email": "ahmed.benali@example.com",
      "department": "علوم الحاسوب",
      "photo": "https://example.com/static/uploads/ahmed_benali_ahmed.jpg",
      "role": "مستخدم"
    }
  }
  ```

- **400 طلب غير صالح** (حقول مطلوبة مفقودة):
  ```json
  {"error": "حقول مطلوبة مفقودة"}
  ```

- **400 طلب غير صالح** (صيغة بريد إلكتروني غير صالحة):
  ```json
  {"error": "صيغة بريد إلكتروني غير صالحة"}
  ```

- **400 طلب غير صالح** (كلمة مرور قصيرة جدًا):
  ```json
  {"error": "يجب أن تكون كلمة المرور 8 أحرف على الأقل"}
  ```

- **400 طلب غير صالح** (البريد الإلكتروني مسجل مسبقًا):
  ```json
  {"error": "البريد الإلكتروني مسجل مسبقًا"}
  ```

- **400 طلب غير صالح** (نوع ملف غير صالح أو غير مدعوم للصورة):
  ```json
  {"error": "نوع ملف غير صالح أو غير مدعوم"}
  ```

- **400 طلب غير صالح** (رابط صورة غير صالح):
  ```json
  {"error": "رابط صورة غير صالح"}
  ```

- **500 خطأ داخلي في الخادم**:
  ```json
  {"error": "فشل في تسجيل المستخدم"}
  ```

## مثال JavaScript (واجهة المستخدم)

```javascript
async function registerUser(userData, isFormData = false) {
  try {
    const url = 'https://educonnect-wp9t.onrender.com/api/register';
    let options = {
      method: 'POST',
      credentials: 'include' // مطلوب لإرسال ملفات تعريف الارتباط للجلسة
    };

    if (isFormData) {
      // لـ form-data (مثال: مع رفع ملف)
      const formData = new FormData();
      for (const key in userData) {
        formData.append(key, userData[key]);
      }
      options.body = formData;
    } else {
      // لـ JSON
      options.headers = { 'Content-Type': 'application/json' };
      options.body = JSON.stringify(userData);
    }

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'فشل التسجيل');
    }

    console.log('التسجيل ناجح:', data);
    return data;
  } catch (error) {
    console.error('خطأ:', error.message);
    throw error;
  }
}

// الاستخدام مع JSON
const userDataJson = {
  first_name: 'أحمد',
  last_name: 'بنعلي',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'علوم الحاسوب',
  skills: 'Python,JavaScript',
  photo_url: 'https://example.com/photos/ahmed.jpg'
};

registerUser(userDataJson)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// الاستخدام مع Form-data (مثال: مع رفع ملف)
const userDataForm = {
  first_name: 'أحمد',
  last_name: 'بنعلي',
  email: 'ahmed.benali@example.com',
  password: 'securepassword123',
  department: 'علوم الحاسوب',
  skills: 'Python,JavaScript',
  photo: document.querySelector('input[type="file"]').files[0] // مثال إدخال ملف
};

registerUser(userDataForm, true)
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