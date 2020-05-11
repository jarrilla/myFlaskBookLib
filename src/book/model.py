# user_book_entry.model.py
# This table yields a way for users to add personal details to any book.
# notes & date_purchased are set by users but specific to a select book from their pov.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  title = db.Column( db.String(120), index=True, unique=True )
  author = db.Column( db.String(64) )

  def __repr__(self):
    return '[Book: title={}, author={}]'.format( self.title, self.author )

# UserBookEntry Model
class UserBookEntry(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  date_purchased = db.Column( db.DateTime )
  notes = db.Column( db.Text )
  book_id = db.Column( db.Integer, db.ForeignKey('book.id') )