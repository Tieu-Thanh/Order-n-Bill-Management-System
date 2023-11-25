import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '0ur_$ecret_K3y'
    # Add other configuration settings here


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
