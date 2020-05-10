from flask import Flask
from config import Config

def create_app(configClass=Config):
  app = Flask(__name__, template_folder='../templates')

  from src.main import bp as main_bp
  app.register_blueprint(main_bp)

  return app