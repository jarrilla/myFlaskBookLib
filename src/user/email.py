from flask import render_template, current_app
from src.email import send_email

# Send a verification email to the specified user
def send_verification_email(user):
  token = user.get_verification_token()
  send_email('[MyFlaskLib] Verify Your Account',
    sender=current_app.config['ADMINS'][0],
    recipients=[user.email],
    text_body=render_template('email/verify_account.txt', user=user, token=token),
    html_body=render_template('email/verify_account.html', user=user, token=token),
  )