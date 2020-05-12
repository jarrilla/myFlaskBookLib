# book.email.py
# Methods for sending emails related to books, collection, etc..
# for now only share_library

from flask import render_template, current_app
from src.email import send_email

# Send an email to a specified address sharing  the user's library link
def send_share_email(user, recipient):
  msg = '[MyFlaskLib] Your Friend '

  send_email('[MyFlaskLib] Your Friend Wants to Share a Collection!',
    sender=current_app.config['ADMINS'][0],
    recipients=[recipient],
    text_body=render_template('email/share_library.txt', user=user),
    html_body=render_template('email/share_library.html', user=user)
  )