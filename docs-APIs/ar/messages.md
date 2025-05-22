# وثائق واجهات برمجة التطبيقات للرسائل (Messages APIs)

## رابط الخادم
`https://educonnect-wp9t.onrender.com`  
استبدل هذا المسار بـ `http://127.0.0.1:5000` إذا كنت تعمل في بيئة الاختبار.

## نظرة عامة
توفر واجهات برمجة التطبيقات الخاصة بالرسائل أدوات لإرسال رسائل بين المستخدمين واسترجاع الرسائل بين مستخدمين اثنين. تتطلب جميع نقاط النهاية جلسة مستخدم نشطة للمصادقة.

## المتطلبات الأساسية
- **الخادم**: يعمل على `https://educonnect-wp9t.onrender.com` في الإنتاج.
- **المصادقة**: يجب أن يكون لدى المستخدم جلسة نشطة (مع `user_id` في الجلسة) للوصول إلى نقاط النهاية.
- **نوع المحتوى**: `application/json` للطلبات التي تحتوي على جسم.
- **HTTPS**: يُوصى به في الإنتاج لحماية البيانات الحساسة.
- **الجلسات**: يتم استخدام الجلسات لتتبع حالة تسجيل الدخول. يجب أن تدعم المتصفحات ملفات تعريف الارتباط (cookies) للجلسات.

## نقاط النهاية (Endpoints)

### 1. إرسال رسالة
- **الطريقة**: `POST`
- **الرابط**: `/messages`
- **الوصف**: إرسال رسالة جديدة من المستخدم الحالي إلى مستخدم آخر.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

#### جسم الطلب
| الحقل           | النوع   | الوصف         | ملاحظات               |
| --------------- | ------- | ------------- | --------------------- |
| `receiver_id` * | Integer | معرف المستلم  | مطلوب                 |
| `content` *     | String  | محتوى الرسالة | لا يمكن أن يكون فارغًا |

**مثال**:
```json
{
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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
const messageData = {
  receiver_id: 2,
  content: "Hello, how's the project going?"
};

sendMessage(messageData)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 2. استرجاع الرسائل بين مستخدمين
- **الطريقة**: `GET`
- **الرابط**: `/messages/<other_user_id>`
- **الوصف**: استرجاع الرسائل بين المستخدم الحالي ومستخدم آخر، مُصفحة.
- **المصادقة**: مطلوبة (جلسة مستخدم نشطة).

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

#### مثال JavaScript (Frontend):
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

// استخدام الدالة
getMessages(2, 1, 30)
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

## ملاحظات عامة
- يُوصى باستخدام HTTPS في الإنتاج لحماية البيانات الحساسة.
- اختبر الواجهات باستخدام أدوات مثل Postman أو cURL.
- يجب تمكين ملفات تعريف الارتباط (cookies) في المتصفح لدعم إدارة الجلسات.
- للواجهات التي تتطلب المصادقة، يتم التحقق من وجود جلسة نشطة تحتوي على `user_id`.
- يتم تسجيل الإجراءات المتعلقة بإرسال الرسائل باستخدام `AuditLogManager` لأغراض التدقيق.
- لتحسين الأمان، تأكد من أن ملفات تعريف الارتباط للجلسة تُرسل مع خاصية `HttpOnly` و`Secure` في بيئة الإنتاج.
- مدة الجلسة تعتمد على إعداد `PERMANENT_SESSION_LIFETIME` في الخادم.
- يتم منع إرسال الرسائل إلى نفس المستخدم (المرسل والمستلم لا يمكن أن يكونا نفس الشخص).