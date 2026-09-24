# Project Name
الذكريات (Alzikrayat) - Memory App

# A simple Description
تطبيق ويب تفاعلي يتيح للمستخدمين إنشاء حسابات شخصية، مشاركة صورهم وذكرياتهم، والتفاعل مع ذكريات الآخرين عبر التعليقات. تم بناء التطبيق مع التركيز على تطبيق معمارية (MVC) برمجية نظيفة وإدارة قواعد البيانات بشكل مباشر.

# Technologies
- **Backend:** Python, Flask
- **Database:** MySQL, PyMySQL (Raw SQL Queries without ORM)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Security:** bcrypt (Password Hashing)

# How to run
1. إنشاء وتفعيل البيئة الافتراضية:
   `python3 -m venv venv`
   `source venv/bin/activate`
2. تثبيت المكتبات المعتمدة:
   `pip install -r requirements.txt`
3. إعداد قاعدة البيانات:
   - قم بتشغيل خادم MySQL وإنشاء قاعدة بيانات باسم `alzikrayat`.
   - تأكد من تعيين بيانات الاتصال في ملف `app/config.py` (المستخدم `root`).
4. تشغيل الخادم:
   `python3 run.py`
5. تصفح التطبيق عبر الرابط: `http://127.0.0.1:5000`

# Student Name
Abd Alwhab Mohammed Saeed