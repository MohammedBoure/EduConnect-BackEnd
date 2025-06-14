import requests

# إعداد عنوان الـ API (تأكد من استبداله بعنوان السيرفر الفعلي)
url = "http://localhost:5000/api/admin/messages/4"  # الرسالة رقم 4

# إرسال طلب DELETE إلى الـ API
response = requests.delete(url)

# طباعة حالة الاستجابة والنص الناتج
print("Status Code:", response.status_code)
print("Response Text:", response.text)
