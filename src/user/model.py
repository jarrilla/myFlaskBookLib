from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
  id = db.Column( db.Integer, primary_key=True )
  username = db.Column( db.String(64), index=True, unique=True )
  email = db.Column( db.String(120), index=True, unique=True )
  password_hash = db.Column( db.String(128) )
  is_verified = db.Column( db.Boolean, default=False, nullable=False )

  def __repr__(self):
    return '[User: id={}, username={}, email={}, is_verified={}]'.format(
      self.id, self.username, self.email, self.is_verified
    )

# Set a User's password_hash
# Used when registering or resetting password
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

# Check a given raw password vs saved pwd hash
# Used for login
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
