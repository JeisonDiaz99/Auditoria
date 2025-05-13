from os import environ


class BaseConfig:
    SECRET_KEY = environ.get('SECRET_APP_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = environ.get('API_KEY', 'your_api_key')
    N8N_WEBHOOK_URL = environ.get('N8N_WEBHOOK_URL', 'https://primary-production-43086.up.railway.app/webhook-test/cdd85273-e3f8-434f-8b24-521f8c5fdb37')
    

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DB_URL', 'sqlite:///docs.db')
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USERNAME = environ.get('MAILTRAP_USERNAME')
    MAIL_PASSWORD = environ.get('MAILTRAP_PASSWORD')
    DONT_REPLY_FROM_EMAIL =environ.get('TEST_EMAIL')
    MAIL_USE_TLS = True
    DEBUG = True  # Enable debug mode in development
    
    

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URL')
    DEBUG = False  # Disable debug mode in production
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USERNAME = environ.get('ADMINISTER_EMAIL')
    MAIL_PASSWORD = environ.get('APP_PASSWORD_EMAIL')
    MAIL_USE_TLS = True
    

class Settings:
    """Configuration factory."""
    """@autor:Kevin Acuña,
    @version: v1 09/04/2025
    @description: This class contains the settings for the application.
    """
    environment: str = environ.get("APP_ENV", "development")
    
    @staticmethod
    def get_config():
        env = Settings.environment
        if env == "development":
            return DevelopmentConfig
        elif env == "production":
            return ProductionConfig
        else:
            raise ValueError(f"Unknown environment: {env}")