# user.forms.py
# Forms used by User endpoints.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from src.user.model import User

# Basic User registration form
# Username, Email, Password are all required
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(),
    EqualTo('password', message='Passwords must match.')
  ])
  submit = SubmitField('Register')

# Usernames must be unique
  def validate_username(self, username):
    user = User.query.filter_by( username=username.data ).first()
    if user is not None:
      raise ValidationError('That username already exists!')

# Email must be unique
  def validate_email(self, email):
    user = User.query.filter_by( email=email.data ).first()
    if user is not None:
      raise ValidationError('That email is already registered!')

# Basic User Login form
# Username and Passwort are required
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')