from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user

from src import db
from src.models import User, UserBookEntry
from src.book import bp
from src.book.forms import NewEntryForm

# library()
# Show a specific user's library
@bp.route('/library/<username>')
@login_required
def library(username):
  user = User.query.filter_by(username=username).first_or_404()
  entries = user.collection().all()

  return render_template('library.html', user=user, entries=entries)

# edit_library()
# Allow user to edit their collection
@bp.route('/edit_library', methods=['GET', 'POST'])
@login_required
def edit_library():
  form = NewEntryForm()
  if form.validate_on_submit():
    title = form.title.data
    author = form.author.data
    date_purchased = form.date_purchased.data
    notes = form.notes.data

    entry = current_user.add_entry_to_collection(
      title=title, author=author, date_purchased=date_purchased, notes=notes
    )

    if entry is not None:
      try:
        db.session.commit()
      except Exception as e:
        flash('Error adding book your collection.')

      return redirect( url_for('book.library', username=current_user.username) )
    
  return render_template('edit_library.html', user=current_user, form=form)