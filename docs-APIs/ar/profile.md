# وثائق واجهات برمجة التطبيقات للملفات الشخصية (Profile APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الخاصة بالملفات الشخصية أدوات لإدارة ملفات تعريف المستخدمين، بما في ذلك استرجاع تفاصيل المستخدم، تحديث الملف الشخصي، حذف الملف الشخصي، والبحث عن ملفات تعريف بناءً على معايير معينة. معظم نقاط النهاية تتطلب جلسة مستخدم نشطة للمصادقة، باستثناء استرجاع تفاصيل مستخدم معين.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة (مع `user_id` في الجلسة) للوصول إلى نقاط النهاية التي تتطلب المصادقة (تحديث، حذف، أو البحث).
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. استرجاع ملف المستخدم
- **الطريقة**: `GET`
- **الرابط**: `/profile/<user_id>`
- **الوصف**: استرجاع تفاصيل مستخدم محدد بناءً على المعرف.
- **المصادقة**: غير مطلوبة.

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
async function getProfile(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/profile/${userId}`, {
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
getProfile(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. تحديث ملف المستخدم

- **الطريقة**: `PUT`
- **الرابط**: `/api/profile/<user_id>`
- **الوصف**: تحديث بيانات ملف المستخدم. يدعم طلبات JSON أو form-data. يمكن للمستخدمين تحديث الصورة الشخصية عبر رفع ملف أو رابط URL (بما في ذلك روابط بيانات Base64).
- **المصادقة**: مطلوبة (JWT، يمكن لمالك الملف فقط التحديث).
- **نوع المحتوى**: `application/json` أو `multipart/form-data`

## معلمات المسار

| المعلم       | النوع   | الوصف             | ملاحظات            |
| ------------- | ------- | ----------------- | ------------------ |
| `user_id` *   | عدد صحيح | معرف المستخدم    | عدد صحيح إيجابي   |

## جسم الطلب

| الحقل        | النوع        | الوصف               | ملاحظات                                            |
| ------------- | ------------ | ------------------- | -------------------------------------------------- |
| `first_name`  | نص           | الاسم الأول        | اختياري                                           |
| `last_name`   | نص           | الاسم الأخير       | اختياري                                           |
| `department`  | نص           | القسم أو التخصص    | اختياري                                           |
| `skills`      | مصفوفة/نص   | قائمة المهارات     | اختياري، يمكن أن تكون مصفوفة أو سلسلة مفصولة بفواصل |
| `photo`       | ملف          | ملف الصورة الشخصية | اختياري؛ الأنواع المدعومة: PNG، JPG، JPEG (يُستخدم مع `multipart/form-data`) |
| `photo_url`   | نص           | رابط الصورة الشخصية | اختياري؛ يجب أن يكون رابط HTTP/HTTPS أو Base64 (مثال: `data:image/png;base64,...`) |
| `email`       | نص           | البريد الإلكتروني  | اختياري                                           |
| `password`    | نص           | كلمة المرور        | اختياري، 8 أحرف على الأقل                        |

**ملاحظات**:
- الحقل `role` غير مدعوم للتحديث عبر هذه الواجهة لمنع التلاعب بالصلاحيات.
- إذا تم تقديم كل من `photo` و `photo_url`، يتم الأولوية لملف `photo` المرفوع.
- يجب تقديم حقل واحد على الأقل للتحديث.

**مثال (JSON)**:
```json
{
  "first_name": "أحمد",
  "last_name": "محمد",
  "department": "هندسة البرمجيات",
  "skills": ["Python", "Java", "SQL"],
  "photo_url": "https://example.com/photos/ahmed_new.jpg",
  "email": "ahmed.mohamed@example.com"
}
```

**مثال (Form-data)**:
```
first_name: أحمد
last_name: محمد
department: هندسة البرمجيات
skills: Python,Java,SQL
photo: (ملف ثنائي، مثال: ahmed_new.jpg)
email: ahmed.mohamed@example.com
```

## الردود

- **200 ناجح**:
  ```json
  {
    "message": "تم تحديث المستخدم بنجاح",
    "user": {
      "id": 123,
      "first_name": "أحمد",
      "last_name": "محمد",
      "email": "ahmed.mohamed@example.com",
      "department": "هندسة البرمجيات",
      "skills": ["Python", "Java", "SQL"],
      "photo": "https://example.com/static/uploads/ahmed_mohamed_ahmed_new.jpg",
      "role": "مستخدم"
    }
  }
  ```

- **400 طلب غير صالح** (لم يتم تقديم بيانات للتحديث):
  ```json
  {"error": "لم يتم تقديم بيانات للتحديث"}
  ```

- **400 طلب غير صالح** (لم يتم تقديم حقول صالحة للتحديث):
  ```json
  {"error": "لم يتم تقديم حقول صالحة للتحديث"}
  ```

- **400 طلب غير صالح** (نوع ملف غير صالح أو غير مدعوم للصورة):
  ```json
  {"error": "نوع ملف غير صالح أو غير مدعوم"}
  ```

- **400 طلب غير صالح** (رابط صورة غير صالح):
  ```json
  {"error": "صيغة رابط صورة غير صالحة"}
  ```

- **403 ممنوع** (محاولة تحديث حقل `role`):
  ```json
  {"error": "غير مصرح: لا يمكن تحديث الدور عبر هذه الواجهة"}
  ```

- **403 ممنوع** (محاولة تحديث ملف مستخدم آخر):
  ```json
  {"error": "غير مصرح: يمكنك فقط تحديث ملفك الشخصي"}
  ```

- **404 غير موجود**:
  ```json
  {"error": "المستخدم غير موجود"}
  ```

- **500 خطأ داخلي في الخادم**:
  ```json
  {"error": "فشل في تحديث المستخدم"}
  ```

## مثال JavaScript (واجهة المستخدم)

```javascript
async function updateUserProfile(userId, updateData, token, isFormData = false) {
  try {
    const url = `https://educonnect-wp9t.onrender.com/api/profile/${userId}`;
    let options = {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      credentials: 'include' // مطلوب لإرسال ملفات تعريف الارتباط للجلسة
    };

    if (isFormData) {
      // لـ form-data (مثال: مع رفع ملف)
      const formData = new FormData();
      for (const key in updateData) {
        if (Array.isArray(updateData[key])) {
          formData.append(key, updateData[key].join(',')); // تحويل المصفوفة إلى سلسلة مفصولة بفواصل
        } else {
          formData.append(key, updateData[key]);
        }
      }
      options.body = formData;
    } else {
      // لـ JSON
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(updateData);
    }

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'فشل في تحديث الملف الشخصي');
    }

    console.log('تم تحديث الملف الشخصي:', data);
    return data;
  } catch (error) {
    console.error('خطأ:', error.message);
    throw error;
  }
}

// الاستخدام مع JSON
const userId = 123;
const updateDataJson = {
  first_name: 'أحمد',
  last_name: 'محمد',
  department: 'هندسة البرمجيات',
  skills: ['Python', 'Java', 'SQL'],
  photo_url: 'https://example.com/photos/ahmed_new.jpg',
  email: 'ahmed.mohamed@example.com'
};
const jwtToken = 'your_jwt_token_here';

updateUserProfile(userId, updateDataJson, jwtToken)
  .then(data => console.log(data))
  .catch(error => console.error(error));

// الاستخدام مع Form-data (مثال: مع رفع ملف)
const updateDataForm = {
  first_name: 'أحمد',
  last_name: 'محمد',
  department: 'هندسة البرمجيات',
  skills: ['Python', 'Java', 'SQL'],
  photo: document.querySelector('input[type="file"]').files[0], // مثال إدخال ملف
  email: 'ahmed.mohamed@example.com'
};

updateUserProfile(userId, updateDataForm, jwtToken, true)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```
### 3. حذف ملف المستخدم
- **الطريقة**: `DELETE`
- **الرابط**: `/profile/<user_id>`
- **الوصف**: حذف الملف الشخصي للمستخدم المصادق عليه (يجب أن يكون المستخدم هو صاحب الملف).
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### الاستجابات
- **200 OK**:
  ```json
  {"message": "User deleted successfully"}
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

#### مثال JavaScript (Frontend):
```javascript
async function deleteProfile(userId) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/profile/${userId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete profile');
    }
    console.log('Profile deleted successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
deleteProfile(1)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 4. البحث عن ملفات تعريف
- **الطريقة**: `GET`
- **الرابط**: `/search`
- **الوصف**: البحث عن ملفات تعريف المستخدمين بناءً على الاسم الأول، القسم، أو المهارات، مع تصفية مُصفحة.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### معلمات الاستعلام
| المعلمة      | النوع   | الوصف                     | افتراضي |
|--------------|---------|---------------------------|----------|
| `nom`        | String  | الاسم الأول              | فارغ     |
| `filiere`    | String  | القسم/التخصص             | فارغ     |
| `competence` | String  | المهارة                   | فارغ     |
| `page`       | Integer | رقم الصفحة               | 1        |
| `per_page`   | Integer | عدد الملفات لكل صفحة     | 10       |

#### الاستجابات
- **200 OK**:
  ```json
  {
    "results": [
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
async function searchProfiles(params = {}) {
  try {
    const query = new URLSearchParams({
      nom: params.nom || '',
      filiere: params.filiere || '',
      competence: params.competence || '',
      page: params.page || 1,
      per_page: params.per_page || 10
    }).toString();

    const response = await fetch(`https://educonnect-wp9t.onrender.com/search?${query}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to search profiles');
    }
    console.log('Profiles fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const searchParams = {
  nom: 'Ahmed',
  filiere: 'Computer Science',
  competence: 'Python',
  page: 1,
  per_page: 10
};

searchProfiles(searchParams)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة تحتوي على `user_id`.
- يتم تسجيل الإجراءات المتعلقة بتحديث وحذف الملفات الشخصية باستخدام `AuditLogManager` لأغراض التدقيق.
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.
- تحديث وحذف الملفات الشخصية مقيدان بالمستخدم صاحب الملف فقط، ويتم منع تحديث حقل `role` لمنع تصعيد الصلاحيات.
- عند حذف الملف الشخصي، يتم تسجيل خروج المستخدم تلقائيًا عن طريق مسح الجلسة.