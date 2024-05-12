from flask import Flask
from app.routes.filter_routes import filter_routes_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(filter_routes_bp)
    return app

