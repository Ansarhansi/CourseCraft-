import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '..', '.env') # .env file in the 'backend' directory
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-me' # CHANGE THIS!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://user:password@host/db_name' # REPLACE with your MySQL connection string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Example for JWT configuration (if you add JWT later)
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-change-me' # CHANGE THIS!
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    # JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

class DevelopmentConfig(Config):
    DEBUG = True
    # Example: SQLite for simpler development setup if preferred initially
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'dev_app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:yourpassword@localhost/lms_db' # Common local dev setup

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:' # Use in-memory SQLite for tests
    WTF_CSRF_ENABLED = False # Disable CSRF for testing forms if you use Flask-WTF

class ProductionConfig(Config):
    DEBUG = False
    # Ensure DATABASE_URL is set in the production environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # Must be set in prod
    # Add other production-specific settings here, e.g., logging, security headers

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    default=DevelopmentConfig
)

# Helper to get config by name, e.g., for run.py
def get_config_by_name(config_name):
    return config_by_name.get(config_name, DevelopmentConfig)