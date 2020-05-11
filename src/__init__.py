from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

  # Create DB resources
  from src.user.models import User
  from src.book.models import Book, UserBookEntry

  db.init_app(app)
  Migrate(app, db)

  with app.app_context():
    db.create_all()


  # Register blueprints
  from src.main import bp as main_bp
  from src.user import bp as user_bp
  from src.book import bp as book_bp

  app.register_blueprint(main_bp)
  app.register_blueprint(user_bp)
  app.register_blueprint(book_bp)

  return app