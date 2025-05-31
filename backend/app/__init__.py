from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Assuming 'lms/backend' is effectively the root for the 'app' package,
# this import should resolve to lms/backend/app/config.py
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all domains on all routes
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints here
    from .routes import main_bp # .routes is correct as routes.py is in the same 'app' package
    app.register_blueprint(main_bp, url_prefix='/api')

    # Moved health_check to be defined just before returning the app
    @app.route('/health') # Diagnostic route
    def health_check():
        return "Flask app is healthy!", 200

    return app