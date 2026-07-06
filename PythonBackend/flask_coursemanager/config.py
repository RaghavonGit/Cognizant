class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coursemanager.db'
    SECRET_KEY = 'flask-secret-key'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
