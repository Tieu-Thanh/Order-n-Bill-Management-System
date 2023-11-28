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

    # Firebase credentials
    FIREBASE_CREDENTIALS = {
        "type": "service_account",
        "project_id": "order-n-bill-management-system",
        "private_key_id": "d54e9029669ebc75e0196368ef58db5195e20eef",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDs727VGpvQYv2R\nixAH1XX6zGUPdLNl4FJpPY93R0lLohUz7G/x4xOQOEVxlvEKSbpcuNPbOXvXH9oS\nhXzsXLWXcHUtQKT4ZP5TkIQGmxiCWbXOGfwuDv9l37x2vXoc/KqsGc2PXuHwIYWl\nEFlpgKTcfi23rONllVtVPqwr9/lZgMJTzrsKmxsvlbob+Q9CW4Yj5N4MmtE39AGI\n6QFKwoDYMyI+4umnxvsuK5KbJTeVQ0/3YZg1fWGDSt4EUnMqDBjIO+t4cJiigVM5\nQpttg9anlLp0ZVJKe3VWPaAuGpisXgTOQaO2EI+iD5IW3MuagEyr61dTkUs7zA+c\nVZ9wVMQbAgMBAAECggEAMoCCfjfSuGMxKyGaBCFyqUeBzv6P8ooS5s2xU7pFHDLr\nFAs0fTlqhRYJb0G+FPRMHdFjjtm81Mi8QbBkRTkpl6LnxwJ9Z1iXgRZPndzXJ4mZ\nn9mYD/UwaPV8hU6zxZPxiQdi8klGHVn304wdkshR25Gliv315kQkmJHoPuL3KiVH\nvt27cSin3ZxMLbWBvrLDxyNU+tQ0NeQkXlTh9Vs2CaszNuX4yfUuFqUsOgxfSAos\nP0SzvuiExlq90WQwE8t3PxcHtnaYbIHbXrlLB+IeC/JY+ou1pOUnriTRabzIzlWU\nehsi3UYjAWIuK4R94p1JyzXyiRgQObygjTvOqUqWgQKBgQD9GY0bdrJP0fRpfP3+\nI9IjWw61oxSb+w+HDOoi/zDZlYMTpm4qB9leq9I6DgCcN0NlAG1C01e2A80VM1pK\nnCT393cixdaWXjEfJufvvA2KLDtIQsVDziepG4Xn6x6X2WWH7AeWnU15yNoKcIJE\n4VHqB20WAAVEh8P1jqkIFKG8QQKBgQDvpnbfuMeyWHDYgqdviFflaocF09mcNikI\nSNegXcOMc4qQRUUDpzj8j3vyw1dYq5W64v9+dbJLGqHdoez4hXsqz7zCu4oHx/uJ\nxevf2LuOG2wfNt9MEboaWVA9Q4MhoEE1w93/rKMLvbwNlXs2hore4rvo0/LGnq8o\nstxerFSZWwKBgQCHR6HxXPcfzNO7knBb5x+JgEETerAoUv/Qqml2/TlKAy0FUr6t\nPnbDsEj0eMmAtdUS5jCAOGA4TD3QqBsJp/3mf+Gwt1fkFUJiKTRtIfGGue+RxwaT\nIFx4edqPxE8c0LkA9npz2W4wutc4HzyxvlE/Kmr3CFnIcFygInlcdVKhQQKBgF1g\nv3DszuLvEwlJ33PV7Gm32GSs5122vMY9m8cgwdE4NAWC+CE0R0AhqGovMxmZwf3P\n9T2RHqek+O0i6vLrD9Lenu5BpMbjZV+Jfx75lBsLFFYVS2yYe6tIobs9UxsHFmGc\nsCOvYNhyVZP1as0UH4g5UH6oFzDNI/L3vmYlP9GBAoGAPs5i9ToRVtfGoZqScJyb\nkGEwYSKKU22/mroQvKLGEfTeHlWnS7PmlSImRxNqaUdYK4aO20YOTAHYF8KQcDEP\nIURcd1OiNVbqcMGxOxMFaiCftPiVtZ/99FSgVdu6w6la28MMWKnBC6D5zbgiOo3R\nj+1geeYkScBR3Y8DwEEU4Xg=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-w95ta@order-n-bill-management-system.iam.gserviceaccount.com",
        "client_id": "118046068867367491029",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-w95ta%40order-n-bill-management-system.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }


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
