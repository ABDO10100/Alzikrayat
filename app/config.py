import pymysql

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    
    Returns:
        pymysql.connections.Connection: The database connection object.
        Returns None if the connection fails.
    """
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',          # قم بتعديل اسم المستخدم إذا لزم الأمر
            password='root',          # أضف كلمة المرور الخاصة بقاعدة البيانات إن وجدت
            database='alzikrayat',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        return None
