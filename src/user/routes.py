from flask import flash, render_template, url_for, redirect

from src.user.forms import RegistrationForm
from src.user.model import db, User
from src.user import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User( username=form.username.data, email=form.email.data )
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You have succesfully registed! Check your email to verify your account.')
    return redirect( url_for('main.index') ) ## TODO: change me to user.login
  return render_template('register.html', title='Register', form=form)