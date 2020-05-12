from flask import Blueprint

bp = Blueprint('book', __name__)

from src.book import routes