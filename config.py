import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET-KEY-1234567890')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///trading.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
