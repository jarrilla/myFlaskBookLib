from flask import render_template, url_for

from src.main import bp
from src.models import Book

@bp.route('/')
@bp.route('/index')
def index():
  books = Book.query.all()
  return render_template('index.html', title='Home', books=books)