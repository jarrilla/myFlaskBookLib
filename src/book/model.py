# book.model.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Book model
# We make the assumption that books have unique titles so that we can use the field as an index
# We could add ISBNs which would be unique but for the purposes of this app, that seems like overkill
class Book(db.Model):
  id = db.Column( db.Integer, primary_key=True )
  title = db.Column( db.String(120), index=True, unique=True )
  author = db.Column( db.String(64) )

  def __repr__(self):
    return '[Book: title={}, author={}]'.format( self.title, self.author )

