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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:congxinzhiyu1?@49.235.89.185/congxinzhiyu_xcx'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 7200