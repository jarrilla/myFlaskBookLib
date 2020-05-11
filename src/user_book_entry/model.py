# user_book_entry.model.py
# This table yields a way for users to add personal details to any book.
# notes & date_purchased are set by users but specific to a select book from their pov.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# UserBookEntry Model
class UserBookEntry(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  date_purchased = db.Column( db.DateTime )
  notes = db.Column( db.Text )
  book_id = db.Column( db.integer, db.ForeignKey('book.id') )