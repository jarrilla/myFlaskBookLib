from config import Config
from flask import Flask
from flask_login import LoginManager

login = LoginManager()
login.login_view = 'user.login'
login.login_message = 'Login or Register to manage your library'

def create_app(config_class=Config):
  app = Flask(__name__, template_folder='../templates')
  app.config.from_object(config_class)

  login.init_app(app)

  from src.main import bp as main_bp
  from src.user import bp as user_bp
  from src.user.model import db as user_db

  # Create DB resources
  user_db.init_app(app)
  with app.app_context():
    user_db.create_all()

  # Register blueprint routes
  app.register_blueprint(main_bp)
  app.register_blueprint(user_bp)

  return app