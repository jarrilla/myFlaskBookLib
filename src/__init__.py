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
  from src.user_book_entry import bp as user_book_entry_bp
  from src.user.model import db as user_db
  from src.book.model import db as book_db
  from src.user_book_entry.model import db as user_book_entry_db

  # Create DB resources
  user_db.init_app(app)
  book_db.init_app(app)
  user_book_entry_db.init_app(app)

  with app.app_context():
    user_db.create_all()
    book_db.create_all()
    user_book_entry_db.create_all()


  # Register blueprint routes
  app.register_blueprint(main_bp)
  app.register_blueprint(user_bp)
  app.register_blueprint(user_book_entry_bp)

  return app