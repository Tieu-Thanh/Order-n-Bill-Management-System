import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '0ur_$ecret_K3y'

    # Add other configuration settings here
    # Firebase configuration
    FIREBASE_API_KEY = "AIzaSyCX8V6ryD-5rhebSJZsL4ichQo8hKWdrXk"
    FIREBASE_AUTH_DOMAIN = "order-n-bill-management-system.firebaseapp.com"
    FIREBASE_PROJECT_ID = "order-n-bill-management-system"
    FIREBASE_STORAGE_BUCKET = "order-n-bill-management-system.appspot.com"
    FIREBASE_MESSAGING_SENDER_ID = "553429788733"
    FIREBASE_APP_ID = "1:553429788733:web:6cafb5155afa9485ae2254"
    FIREBASE_MEASUREMENT_ID = "G-8HRHW115CB"


class DevelopmentConfig(Config):
    DEBUG = True
    # Add development-specific configurations if needed


class TestingConfig(Config):
    TESTING = True
    # Add testing-specific configurations if needed


class ProductionConfig(Config):
    # Add production-specific configurations if needed
    pass


# Determine the current environment and use the appropriate configuration
config_env = os.environ.get('FLASK_ENV', 'development')
if config_env == 'production':
    app_config = ProductionConfig()
elif config_env == 'testing':
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
