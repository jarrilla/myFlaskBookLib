from flask import render_template
from flask_login import login_required

from src.user.model import User

from src.user_book_entry import bp
from src.user_book_entry.model import UserBookEntry

@bp.route('/library/<username>')
@login_required
def library(username):
  user = User.query.filter_by(username=username).first_or_404()
  
  return render_template('library.html', user=user)