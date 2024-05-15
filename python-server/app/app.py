from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from routes.upload_router import upload_controller_bp  # Import your router blueprint
from utils.config import IP_OF_REACT
import jobs.daily_cleanup
from utils.custom_logger import CustomLogger
from configs.app_config import *

logger_manager = CustomLogger("app/logs/app.log",True)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True,origins= IP_OF_REACT)
    ma = Marshmallow(app)
    logger_manager.info("yes this is it ")
    app.register_blueprint(upload_controller_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True ,port=PORT) 