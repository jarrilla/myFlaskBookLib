from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user

from src import db
from src.models import User, UserBookEntry
from src.book import bp
from src.book.email import send_share_email
from src.book.forms import NewEntryForm, EditEntryMetaForm, ShareLibraryForm

# library()
# Show a specific user's library
@bp.route('/library/<username>')
@login_required
def library(username):
  user = User.query.filter_by(username=username).first_or_404()

  page = request.args.get('page', 1, type=int)
  entries = user.collection().paginate(
    page,
    current_app.config['ENTRIES_PER_PAGE'],
    False
  )

  next_url = url_for( 'book.library', username=username, page=entries.next_num ) if entries.has_next else None
  prev_url = url_for( 'book.library', username=username, page=entries.prev_num ) if entries.has_prev else None

  return render_template('library.html', user=user, entries=entries.items, next_url=next_url, prev_url=prev_url)

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

# add_to_lib()
# Add a specified book to user's collection
@bp.route('/add_to_lib/<int:book_id>')
@login_required
def add_to_lib(book_id):

  result = current_user.insert_book_id_to_collection(book_id)
  db.session.commit()

  if result is None:
    flash('Error occurred adding book to your library.')
  elif result is True:
    flash('Book was added to your collection!')
  else:
    flash('That book is already in your collection.')
  
  return redirect( url_for('book.library', username=current_user.username) )

# remove_entry()
# Remove a specified book entry from user's collection
@bp.route('/remove_entry/<int:entry_id>')
@login_required
def remove_entry(entry_id):
  entry = UserBookEntry.query.get(entry_id)
  if entry.owner != current_user:
    flash('You do not have permission to access that resource!')

  else:
    db.session.delete(entry)
    db.session.commit()
    flash('Book has been removed from your collection.')

  return redirect( url_for('book.library', username=current_user.username) )

# share_library()
# Share current_user's library with friends
@bp.route('/share_library', methods=['GET', 'POST'])
@login_required
def share_library():
  form = ShareLibraryForm()
  if form.validate_on_submit():
    recipient = form.recipient.data
    send_share_email(user=current_user, recipient=recipient)
    flash('Email has been sent!')

    return redirect( url_for('book.library', username=current_user.username) )

  return render_template('share_library.html', form=form)