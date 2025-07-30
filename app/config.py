import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.getenv('SECRET_KEY')