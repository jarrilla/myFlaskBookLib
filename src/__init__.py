from flask import Flask
from config import Config

def create_app(config_class=Config):
  app = Flask(__name__, template_folder='../templates')
  app.config.from_object(config_class)

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