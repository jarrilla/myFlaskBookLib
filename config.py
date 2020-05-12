import os

# project base directory.. used to define dev DB path
baseDir = os.path.abspath(os.path.dirname(__file__))

class TestConfig:
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
  # cookie encoding secret
  SECRET_KEY = os.environ.get('SECRET_KEY') or \
    'someSecret12345'

  # DB 
  SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
    'sqlite:///' + os.path.join(baseDir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # entries to show per page
  # this is intentionally a low number to showcase the feature
  ENTRIES_PER_PAGE=5

  # MAILER vars
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = os.environ.get('MAIL_PORT') or 25
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = ['ja.dev.mailer@gmail.com']

  # Heroku wants stdout logging
  LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')