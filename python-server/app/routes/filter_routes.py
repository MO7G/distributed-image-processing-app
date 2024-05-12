from flask import Blueprint
from app.controller.filterController import home, sample

# Define a Blueprint for the routes
filter_routes_bp = Blueprint('routes', __name__)

# Define routes
@filter_routes_bp.route('/')
def index():
    return home()

@filter_routes_bp.route('/sample')
def sample_route():
    return sample()
