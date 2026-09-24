from app import app
from flask import request
from app.controllers.auth_controller import AuthController

# ==========================================
# 1. مسارات الصفحات الرئيسية والصور (Photos)
# ==========================================

@app.route('/', methods=['GET'])
def index():
    """
    Entry point of the application.
    Delegates to PhotoController to show the main gallery or welcoming page.
    """
    from app.controllers.photo_controller import PhotoController
    return PhotoController.index()

@app.route('/photo/<int:photoId>', methods=['GET'])
def showPhoto(photoId):
    """
    Captures the parameterized URL for a specific photo ID.
    Delegates orchestration manually to the PhotoController.
    """
    from app.controllers.photo_controller import PhotoController
    return PhotoController.show(photoId)

@app.route('/photo/create', methods=['GET'])
def createPhoto():
    """Shows the upload form for a new photo."""
    from app.controllers.photo_controller import PhotoController
    return PhotoController.create()

@app.route('/photo/store', methods=['POST'])
def storePhoto():
    """Handles the submission of the photo upload form."""
    from app.controllers.photo_controller import PhotoController
    return PhotoController.store(request)

@app.route('/photo/<int:photoId>/delete', methods=['POST'])
def deletePhoto(photoId):
    """Handles the deletion of a specific photo, verifying ownership first."""
    from app.controllers.photo_controller import PhotoController
    return PhotoController.delete(photoId)

# ==========================================
# 2. مسارات المصادقة (Authentication)
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles both displaying the login form and processing the login submission."""
    from app.controllers.auth_controller import AuthController
    if request.method == 'POST':
        return AuthController.processLogin(request)
    return AuthController.showLogin()

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration viewing and submission."""
    from app.controllers.auth_controller import AuthController
    if request.method == 'POST':
        return AuthController.processRegister(request)
    return AuthController.showRegister()

@app.route('/logout', methods=['GET'])
def logout():
    """Destroys the user session and redirects to the home page."""
    from app.controllers.auth_controller import AuthController
    return AuthController.logout()

# ==========================================
# 3. مسارات التعليقات (Comments)
# ==========================================

@app.route('/photo/<int:photoId>/comment', methods=['POST'])
def storeComment(photoId):
    """Stores a new text comment associated with a specific photo."""
    # سيتم إنشاء CommentController لاحقاً إذا احتجنا لفصله، 
    # أو يمكن معالجته عبر PhotoController
    from app.controllers.photo_controller import PhotoController
    return PhotoController.storeComment(photoId, request)

app.add_url_rule('/profile/edit', 'edit_profile', AuthController.edit_profile, methods=['GET', 'POST'])
