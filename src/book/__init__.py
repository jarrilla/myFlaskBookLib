from flask import Blueprint

bp = Blueprint('user_book_entry', __name__)

from src.book import routes