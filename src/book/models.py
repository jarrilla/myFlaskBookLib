# book.models.py
# The models here are Book and UserBookEntry
#
# - Every user can have multiple UserBookEntries
# - Books are independent entities which can be pointed to by UserBookEntries
# - Each UserBookEntry points to exactly one Book,
#   but any Book can be pointed by up to N UserBookEntires (N = #registered users)
# - A specific user's UserBookEntires are 1-1 with a specific book

from flask_sqlalchemy import SQLAlchemy

from src import db

# Book
# Books entities don't care about which UserBookEntires point to them
class Book(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  title = db.Column( db.String(120), index=True, unique=True )
  author = db.Column( db.String(64) )

  def __repr__(self):
    return '[Book: title={}, author={}]'.format( self.title, self.author )

# UserBookEntry
# 
class UserBookEntry(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  date_purchased = db.Column( db.DateTime )
  notes = db.Column( db.Text )

  book_id = db.Column( db.Integer, db.ForeignKey('book.id') )
  book = db.relationship('Book')
