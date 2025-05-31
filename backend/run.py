import os
from app import create_app, db # db might not be used here directly but often is for shell context
from app.config import get_config_by_name, DevelopmentConfig # Ensure DevelopmentConfig is available if needed as default

# Determine the configuration to use (e.g., from FLASK_CONFIG environment variable)
# Defaults to 'dev' if not set.
config_name = os.getenv('FLASK_CONFIG') or 'dev'
# Ensure get_config_by_name returns a class, not an instance, if create_app expects a class
# Or, if it returns an instance, ensure create_app handles it.
# Based on your config.py, get_config_by_name returns a class.
app = create_app(get_config_by_name(config_name))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Use app.config.get('DEBUG', False) to respect the config's debug setting
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', True)) # Defaulting debug to True for dev