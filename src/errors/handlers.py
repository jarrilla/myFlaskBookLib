# errors.handlers.py
# Very basic error handling for 404 & 500
# Upon 500, do a DB rollback to avoid data corruption

from flask import render_template

from src import db
from src.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('errors/500.html'), 500