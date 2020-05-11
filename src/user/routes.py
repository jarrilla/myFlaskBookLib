from flask import flash, render_template, url_for, redirect, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

from src.user.forms import RegistrationForm, LoginForm
from src.user.model import db, User
from src.user import bp

# User registration route
# - GET:  show view
# - POST: send new user data
@bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User( username=form.username.data, email=form.email.data )
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You have succesfully registered! Check your email to verify your account.')
    return redirect( url_for('user.login') )
    
  return render_template('register.html', title='Register', form=form)

# User login route
# - GET:  show view
# - POST: send login credentials
@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect( url_for('main.index') )
  
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by( username=form.username.data ).first()
    if user is None or not user.check_password( form.password.data ):
      flash('Invalid username or password')
      return redirect( url_for('user.login') )

    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('main.index')
    
    flash('Login successful!')
    return redirect( next_page )

  return render_template('login.html', title='Sign In', form=form)

# User logout route
# - GET:  show view
# - POST: send logout request
@bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect( url_for('main.index') )