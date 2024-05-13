from flask import Blueprint
from controller.upload_controller import upload_file, hello

# Define a Blueprint for the routes
upload_controller_bp = Blueprint('routes', __name__)

# Define routes
@upload_controller_bp.route('/upload' , methods=['POST'])
def index_upload():
    return upload_file()

@upload_controller_bp.route('/', methods=['get'])
def index_hello():
    return hello()


