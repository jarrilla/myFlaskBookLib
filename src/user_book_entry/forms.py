# user_book_entry.forms.py
# Forms used by UserBookEntry endpoints
# Create new entries or edit existing ones.

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from src.user_book_entry.model import UserBookEntry

# Basic UserBookEntry creation form
# This also double as a 'Book' creation form. If the book the user is adding doesn't exist in Book db, we create it
class NewEntryForm(FlaskForm):
  title = StringField('Book Title', validators=[DataRequired()])
  author = StringField('Book Auhtor', validators=[DataRequired()])
  date_purchased = DateField('Date Purchased')
  notes = TextAreaField('Notes')
  submit = SubmitField('Add')

# NOTE(jarrilla):
# We don't need custom validators for Title b/c even though they will be 'unique' we don't want to bog down the user
#   if they're trying to add a book that matches an existing entry.
# If a match is found, we simply add it.