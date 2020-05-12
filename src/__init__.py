from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os

# mailer
mail = Mail()

# login auth
login = LoginManager()
login.login_view = 'user.login'
login.login_message = 'Login or Register to manage your library'

# Database
db = SQLAlchemy()

def create_app(config_class=Config):
  app = Flask(__name__, template_folder='../templates')
  app.config.from_object(config_class)

  login.init_app(app)
  mail.init_app(app)

  # Create DB resources
  db.init_app(app)
  Migrate(app, db)

  with app.app_context():
    db.create_all()


  # Register blueprints
  from src.errors import bp as errs_bp
  from src.main import bp as main_bp
  from src.user import bp as user_bp
  from src.book import bp as book_bp

  app.register_blueprint(errs_bp)
  app.register_blueprint(main_bp)
  app.register_blueprint(user_bp)
  app.register_blueprint(book_bp)


  # Set up logging
  if not app.debug:
    if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
      secure = None

      if app.config['MAIL_USE_TLS']:
        secure = ()
      mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='MyFlaskLib Exception',
        credentials=auth, secure=secure
      )
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

  if not os.path.exists('logs'):
    os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('--- MyFlaskLib startup ---')

  return app