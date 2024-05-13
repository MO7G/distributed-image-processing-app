from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from routes.upload_router import upload_controller_bp  # Import your router blueprint

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True,origins='http://localhost:3000')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    ma = Marshmallow(app)
    
    # Register your router blueprint
    app.register_blueprint(upload_controller_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
  