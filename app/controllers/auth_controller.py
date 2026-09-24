import bcrypt
from flask import render_template, redirect, session, make_response, request, url_for
from datetime import datetime, timedelta
from app.config import get_db_connection

class AuthController:
    
    @staticmethod
    def showLogin():
        """Displays the login form."""
        return render_template('auth/login.html')
        
    @staticmethod
    def processLogin(request):
        """Authenticates the user, sets session, and creates the Last Login cookie."""
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if not conn:
            return "Database connection failed", 500
            
        try:
            with conn.cursor() as cursor:
                # استخدام استعلام آمن لمنع هجمات SQL Injection
                sql = "SELECT * FROM Users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                
                # التحقق من وجود المستخدم وتطابق كلمة المرور المشفرة
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    
                    # إنشاء الجلسة (Session)
                    session['user_id'] = user['id']
                    session['first_name'] = user['first_name']
                    
                    # إعداد ملف تعريف الارتباط (Cookie) لمدة 7 أيام
                    response = make_response(redirect('/'))
                    expire_date = datetime.now() + timedelta(days=7)
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    response.set_cookie('lastLoginDate', current_time, expires=expire_date)
                    return response
                else:
                    return render_template('auth/login.html', error="Invalid email or password")
        finally:
            conn.close()

    @staticmethod
    def showRegister():
        """Displays the registration form."""
        return render_template('auth/register.html')
        
    @staticmethod
    def processRegister(request):
        """Hashes password securely and inserts the new user into the database."""
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # تشفير كلمة المرور باستخدام Bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO Users (first_name, last_name, email, password) 
                         VALUES (%s, %s, %s, %s)"""
                # تخزين الكلمة المشفرة في قاعدة البيانات بدلاً من النص الواضح
                cursor.execute(sql, (first_name, last_name, email, hashed_password))
            conn.commit()
            return redirect('/login')
        except Exception as e:
            # معالجة خطأ تكرار الإيميل (UNIQUE constraint)
            return render_template('auth/register.html', error="Email already exists or invalid data.")
        finally:
            conn.close()
            
    @staticmethod
    def logout():
        """Clears the session and logs the user out."""
        session.clear()
        return redirect('/login')
    
    @staticmethod
    def edit_profile():
        # التأكد من أن المستخدم مسجل الدخول
        if 'user_id' not in session:
            return redirect(url_for('login'))

        conn = get_db_connection()
        
        # إذا كان الطلب GET، نجلب بيانات المستخدم لعرضها في النموذج
        if request.method == 'GET':
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Users WHERE id = %s", (session['user_id'],))
                user = cursor.fetchone()
            conn.close()
            return render_template('auth/edit_profile.html', user=user)

        # إذا كان الطلب POST، نقوم بتحديث البيانات
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            occupation = request.form.get('occupation', '')
            location = request.form.get('location', '')
            description = request.form.get('description', '')
            password = request.form.get('password', '')

            with conn.cursor() as cursor:
                if password:  # إذا قام بإدخال كلمة مرور جديدة، نقوم بتشفيرها وتحديثها
                    import bcrypt
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("""
                        UPDATE Users 
                        SET first_name=%s, last_name=%s, occupation=%s, location=%s, description=%s, password=%s
                        WHERE id=%s
                    """, (first_name, last_name, occupation, location, description, hashed_password, session['user_id']))
                else:  # إذا ترك الحقل فارغاً، نحدث باقي البيانات فقط
                    cursor.execute("""
                        UPDATE Users 
                        SET first_name=%s, last_name=%s, occupation=%s, location=%s, description=%s
                        WHERE id=%s
                    """, (first_name, last_name, occupation, location, description, session['user_id']))
                
                conn.commit()
            
            # تحديث الاسم في الجلسة الحالية في حال تم تغييره
            session['first_name'] = first_name
            conn.close()
            
            return redirect(url_for('index'))