from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    TESTING = environ.get('TESTING')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = '5f352379324c22463451387a0aec5d2f'
    SESSION_TYPE = 'filesystem'
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('mysql+pymysql://DaaS:flask2020@39.97.219.243/daas')
    # SQLALCHEMY_DATABASE_URI = environ.get('mysql//DaaS:flask2020@39.97.219.243/daas')

    SQLALCHEMY_TRACK_MODIFICATIONS = False