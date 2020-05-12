from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user

from src import db
from src.models import User, UserBookEntry
from src.book import bp
from src.book.forms import NewEntryForm, EditEntryMetaForm

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

# edit_entry()
# Allow user to edit a specific entry
@bp.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
  entry = UserBookEntry.query.get(entry_id)
  if entry.owner != current_user:
    flash('You do not have permission to access that resource.')
    return redirect( url_for('book.library', username=current_user.username) )

  form = EditEntryMetaForm()
  if form.validate_on_submit():
    date_purchased = form.date_purchased.data
    notes = (form.notes.data).strip()

    if date_purchased is not None:
      entry.date_purchased = date_purchased
    if notes != '':
      entry.notes = notes

    if date_purchased is not None or notes != '':
      db.session.commit()
      flash('Successfully edited your entry for {}'.format(entry.book.title))
    
    return redirect( url_for('book.library', username=current_user.username) )

  elif request.method == 'GET':
    form.date_purchased.data = entry.date_purchased
    form.notes.data = entry.notes

  return render_template('edit_entry.html', entry=entry, form=form)