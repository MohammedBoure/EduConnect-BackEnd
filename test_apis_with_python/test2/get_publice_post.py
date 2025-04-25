import requests

def test_get_public_post(post_id):
    # تحديد الـ URL الخاص بالـ API
    url = f'http://127.0.0.1:5000/api/posts/public/{post_id}'
    
    try:
        # إرسال طلب GET إلى الـ API
        response = requests.get(url)
        
        # تحقق من الاستجابة
        if response.status_code == 200:
            print("Post found:")
            print(response.json())  # عرض البيانات المُسترجعة
        elif response.status_code == 404:
            print("Error: Post not found")
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# اختبار الـ API مع معرف المنشور 2
test_get_public_post(3)
