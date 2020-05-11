import os

# project base directory.. used to define dev DB path
baseDir = os.path.abspath(os.path.dirname(__file__))

class TestConfig:
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or \
    'someSecret12345'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
    'sqlite:///' + os.path.join(baseDir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False