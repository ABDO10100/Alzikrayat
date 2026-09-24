from app import app

if __name__ == '__main__':
    # تشغيل الخادم في وضع التطوير على المنفذ 5000
    app.run(debug=True, port=5000)
