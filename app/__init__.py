from flask import Flask

app = Flask(__name__, template_folder='views/templates')
# أضف هذا السطر لتشفير الجلسات (يمكنك تغيير النص إلى أي سلسلة عشوائية)
app.secret_key = 'super_secret_key_for_alzikrayat_app' 

from routes import *
