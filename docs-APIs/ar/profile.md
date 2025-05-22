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
- **الرابط**: `/profile/<user_id>`
- **الوصف**: تحديث تفاصيل الملف الشخصي للمستخدم المصادق عليه (يجب أن يكون المستخدم هو صاحب الملف).
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### جسم الطلب
| الحقل          | النوع   | الوصف                     | ملاحظات                     |
|----------------|---------|---------------------------|-----------------------------|
| `first_name`   | String  | الاسم الأول              | اختياري                    |
| `last_name`    | String  | الاسم الأخير             | اختياري                    |
| `email`        | String  | البريد الإلكتروني        | اختياري، يجب أن يكون صالحًا |
| `password`     | String  | كلمة المرور              | اختياري، لا تقل عن 8 أحرف |
| `department`   | String  | القسم/التخصص             | اختياري                    |
| `skills`       | String/Array | المهارات            | اختياري، مفصولة بفواصل أو قائمة |
| `photo`        | String  | رابط صورة الملف الشخصي   | اختياري                    |

**ملاحظة**: حقل `role` غير مسموح به لمنع تصعيد الصلاحيات.

**مثال**:
```json
{
  "first_name": "Ahmed",
  "last_name": "Benali",
  "email": "ahmed.benali@example.com",
  "password": "newpassword123",
  "department": "Computer Science",
  "skills": ["Python", "JavaScript"],
  "photo": "https://example.com/photos/ahmed.jpg"
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
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: You can only update your own profile"}
  ```
- **403 Forbidden**:
  ```json
  {"error": "Unauthorized: Role cannot be updated via this endpoint"}
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
async function updateProfile(userId, profileData) {
  try {
    const response = await fetch(`https://educonnect-wp9t.onrender.com/profile/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profileData),
      credentials: 'include'
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to update profile');
    }
    console.log('Profile updated successfully:', data);
    return data;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// استخدام الدالة
const profileData = {
  first_name: 'Ahmed',
  last_name: 'Benali',
  email: 'ahmed.benali@example.com',
  password: 'newpassword123',
  department: 'Computer Science',
  skills: ['Python', 'JavaScript'],
  photo: 'https://example.com/photos/ahmed.jpg'
};

updateProfile(1, profileData)
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