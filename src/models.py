from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src import login, db

# user_loader callback
@login.user_loader
def load_user(id):
  return User.query.get(int(id))

# User model
# - username, email are INDEX for faster lookup
# - is_verifed is set to False initally and should only be set to True after a user
#   has verified his/her email
class User(UserMixin, db.Model):
  id = db.Column( db.Integer, primary_key=True )
  username = db.Column( db.String(64), index=True, unique=True )
  email = db.Column( db.String(120), index=True, unique=True )
  password_hash = db.Column( db.String(128) )
  is_verified = db.Column( db.Boolean, default=False )
  library = db.relationship('UserBookEntry', backref='owner', lazy='dynamic')

  def __repr__(self):
    return '[User: id={}, username={}]'.format( self.id, self.username )

  # Set a User's password_hash
  # Used when registering or resetting password
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  # Check a given raw password vs saved pwd hash
  # Used for login
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Get a user's user_book_entry collection (i.e. library) QUERY
  # We return the query so they can decided how to use it (all, paginate, etc..)
  def collection(self):
    return UserBookEntry.query.filter_by(user_id=self.id)

  # Get a UserBookEntry given a book object
  def get_collection_entry_from_book(self, book):
    return self.library.filter_by(book_id=book.id).first()

  # Check if a given book is in the user's collection
  def is_book_in_collection(self, book):
    return self.get_collection_entry_from_book(book) is not None

  # Attempt to add a UserBookEntry to the user's collection.
  # Will not duplicate entry if one already exists
  # Returns the UserBookEntry object matching the given parameters
  def add_entry_to_collection(self, title, author, date_purchased=None, notes=None):
    # get Book entity if it exists
    book = Book.query.filter_by(title=title, author=author).first()
    if book is not None:
      # check if BookEntry exists with that id
      entry = self.get_collection_entry_from_book(book)
      if entry is not None:
        return entry

    # Book doesn't exist, create it
    else:
      book = Book(title=title, author=author)
      db.session.add(book)
      db.session.commit()

    # now create the entry
    entry = UserBookEntry(user_id=self.id, book_id=book.id, notes=notes, date_purchased=date_purchased)
    db.session.add(entry)
    db.session.commit()

    # and add it
    self.library.append(entry)

    return entry

  # Attempt to insert a new entry to user's collection by Book.id
  # Returns None if failed (id is bogus or exception)
  # Returns the (possibly new) entry otherwise
  def insert_book_id_to_collection(self, book_id):
    book = Book.query.get(book_id)
    if book is None:
      return None
    
    if self.is_book_in_collection(book):
      return False

    entry = UserBookEntry(user_id=self.id, book_id=book_id)
    db.session.add(entry)
    db.session.commit()
    self.library.append(entry)

    return True


# - Every user can have multiple UserBookEntries
# - Books are independent entities which can be pointed to by UserBookEntries
# - Each UserBookEntry points to exactly one Book,
#   but any Book can be pointed by up to N UserBookEntires (N = #registered users)
# - A specific user's UserBookEntires are 1-1 with a specific book

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
  date_purchased = db.Column( db.Date )
  notes = db.Column( db.Text )

  user_id = db.Column( db.Integer, db.ForeignKey('user.id') )

  book_id = db.Column( db.Integer, db.ForeignKey('book.id') )
  book = db.relationship('Book')

  def __repr__(self):
    return '[Entry: user_id={}, book_id={}]'.format(self.user_id, self.book_id)
