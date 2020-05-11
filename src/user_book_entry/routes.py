from flask_login import login_required

from src.user_book_entry import bp

# book_entry route
# - GET:  view a specific view entry. If it belongs to the viewing user, allow edits
@bp.route('/book_entry/<entry_id>')
def get_book_entry():
  return

# book_entry @login_required restricted route
@bp.route('/book_entry/<entry_id>', methods=['POST'])
@login_required
def post_book_entry():
  return
