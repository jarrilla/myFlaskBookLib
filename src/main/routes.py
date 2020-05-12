from flask import render_template, url_for, current_app, request
from flask_login import current_user, login_required

from src.main import bp
from src.models import Book, UserBookEntry

@bp.route('/')
@bp.route('/index')
def index():
  page = request.args.get('page', 1, type=int)

  # if user isn't logged in, show every book that other's have added
  # otherwise, show books that others have added which you haven't
  query = None
  if current_user.is_anonymous:
    query = UserBookEntry.query
  else:
    query = UserBookEntry.query.filter( UserBookEntry.user_id != current_user.id )

  entries = query.paginate(
    page,
    current_app.config['ENTRIES_PER_PAGE'],
    False
  )

  next_url = url_for( 'main.index', page=entries.next_num ) if entries.has_next else None
  prev_url = url_for( 'main.index', page=entries.prev_num ) if entries.has_prev else None

  return render_template('index.html', title='Home', entries=entries.items, next_url=next_url, prev_url=prev_url)