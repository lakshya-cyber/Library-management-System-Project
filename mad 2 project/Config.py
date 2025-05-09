class Config(object):
    DEBUG = False
    TESTING = False
    CASH_TYPE = "Rediscache"
    CASH_DEFAULT_TIMEOUT = 300

    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = "thisismysecretkey"
    SECURITY_PASSWORD_SALT = "thisipassword"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CASH_REDIS_HOST = 'localhost'
    CASH_REDIS_PORT = 6379
    CASH_REDIS_DB = 6