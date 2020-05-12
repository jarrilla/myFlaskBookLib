from flask import render_template, url_for, current_app, request
from flask_login import current_user, login_required

from src.main import bp
from src.models import Book, UserBookEntry

@bp.route('/')
@bp.route('/index')
@login_required
def index():
  page = request.args.get('page', 1, type=int)
  books = Book.query.paginate(
    page,
    current_app.config['ENTRIES_PER_PAGE'],
    False
  )

  next_url = url_for( 'main.index', page=books.next_num ) if books.has_next else None
  prev_url = url_for( 'main.index', page=books.prev_num ) if books.has_prev else None

  return render_template('index.html', title='Home', books=books.items, next_url=next_url, prev_url=prev_url)