from flask import render_template, url_for

from src.main import bp

@bp.route('/')
@bp.route('/index')
def index():
  return render_template('index.html', title='Home')