from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from src.user.model import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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