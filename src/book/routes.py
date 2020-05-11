from flask import render_template
from flask_login import login_required

from src.user.models import User

from src.book import bp
from src.book.models import UserBookEntry

@bp.route('/library/<username>')
@login_required
def library(username):
  user = User.query.filter_by(username=username).first_or_404()
  
  return render_template('library.html', user=user)