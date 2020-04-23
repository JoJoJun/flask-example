from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    TESTING = environ.get('TESTING')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = 'a-secret-key'
    SESSION_TYPE = 'filesystem'
    # Database
    # SQLALCHEMY_DATABASE_URI = environ.get('mysql+pymysql://')
    # 之前一直Nonetype 是因为环境变量里没有叫这个的environ
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False