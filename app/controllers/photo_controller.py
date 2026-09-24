import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, session, request
from app.config import get_db_connection

# إعداد مسار حفظ الصور - يُفضل إنشاء مجلد static/images/uploads في المجلد الرئيسي
UPLOAD_FOLDER = 'app/static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class PhotoController:
    
    @staticmethod
    def index():
        """Fetches all photos to display in the main gallery."""
        conn = get_db_connection()
        photos = []
        try:
            with conn.cursor() as cursor:
                # جلب الصور مع اسم صاحب الصورة
                sql = """SELECT Photos.*, Users.first_name, Users.last_name 
                         FROM Photos 
                         JOIN Users ON Photos.user_id = Users.id 
                         ORDER BY date_time DESC"""
                cursor.execute(sql)
                photos = cursor.fetchall()
        finally:
            conn.close()
            
        return render_template('photos/index.html', photos=photos)

    @staticmethod
    def show(photo_id):
        """Displays a single photo with its details and comments."""
        conn = get_db_connection()
        photo = None
        comments = []
        try:
            with conn.cursor() as cursor:
                # 1. جلب تفاصيل الصورة
                photo_sql = """SELECT Photos.*, Users.first_name, Users.last_name 
                               FROM Photos 
                               JOIN Users ON Photos.user_id = Users.id 
                               WHERE Photos.id = %s"""
                cursor.execute(photo_sql, (photo_id,))
                photo = cursor.fetchone()
                
                # 2. جلب التعليقات المرتبطة بالصورة
                if photo:
                    comment_sql = """SELECT Comments.*, Users.first_name, Users.last_name 
                                     FROM Comments 
                                     JOIN Users ON Comments.user_id = Users.id 
                                     WHERE photo_id = %s 
                                     ORDER BY date_time ASC"""
                    cursor.execute(comment_sql, (photo_id,))
                    comments = cursor.fetchall()
        finally:
            conn.close()
            
        if not photo:
            return "Photo not found", 404
            
        return render_template('photos/show.html', photo=photo, comments=comments)

    @staticmethod
    def create():
        """Shows the upload form. Restricted to logged-in users."""
        if 'user_id' not in session:
            return redirect('/login')
        return render_template('photos/create.html')

    @staticmethod
    def store(request):
        """Processes the file upload and saves metadata to the database."""
        if 'user_id' not in session:
            return redirect('/login')
            
        # التحقق من وجود الملف في الطلب
        if 'file' not in request.files:
            return render_template('photos/create.html', error="No file part")
            
        file = request.files['file']
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        if file.filename == '':
            return render_template('photos/create.html', error="No selected file")
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # التأكد من وجود مجلد الرفع
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
                
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    sql = """INSERT INTO Photos (user_id, file_name, title, description) 
                             VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (session['user_id'], filename, title, description))
                conn.commit()
                return redirect('/')
            except Exception as e:
                return render_template('photos/create.html', error="Database error occurred.")
            finally:
                conn.close()
        else:
            return render_template('photos/create.html', error="Invalid file format.")

    @staticmethod
    def delete(photo_id):
        """Deletes a photo after verifying ownership."""
        if 'user_id' not in session:
            return redirect('/login')
            
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 1. التحقق من أن المستخدم الحالي هو صاحب الصورة
                check_sql = "SELECT user_id, file_name FROM Photos WHERE id = %s"
                cursor.execute(check_sql, (photo_id,))
                photo = cursor.fetchone()
                
                if not photo:
                    return "Photo not found", 404
                    
                if photo['user_id'] != session['user_id']:
                    return "Unauthorized action. You can only delete your own photos.", 403
                
                # 2. حذف الملف من السيرفر
                file_path = os.path.join(UPLOAD_FOLDER, photo['file_name'])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                # 3. حذف السجل من قاعدة البيانات
                delete_sql = "DELETE FROM Photos WHERE id = %s"
                cursor.execute(delete_sql, (photo_id,))
            conn.commit()
            return redirect('/')
        finally:
            conn.close()

    @staticmethod
    def storeComment(photo_id, request):
        """Adds a comment to a specific photo."""
        if 'user_id' not in session:
            return redirect('/login')
            
        comment_text = request.form.get('comment')
        
        if comment_text:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    sql = """INSERT INTO Comments (photo_id, user_id, comment) 
                             VALUES (%s, %s, %s)"""
                    cursor.execute(sql, (photo_id, session['user_id'], comment_text))
                conn.commit()
            finally:
                conn.close()
                
        # إعادة توجيه المستخدم إلى نفس صفحة الصورة بعد التعليق
        return redirect(f'/photo/{photo_id}')
