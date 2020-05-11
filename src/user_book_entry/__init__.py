from flask import Blueprint

bp = Blueprint('user_book_entry', __name__)

from src.user_book_entry import routes