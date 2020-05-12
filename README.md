## myFlaskBookLib

Basic Flask app emulating a personal library.

Registered users can add book entries to their library and add notes to any title in their virtual library.


### To run in DEBUG mode
windows:
>\> ./bin/dev.ps1

### Structure
This project is split into 4 modules:
- **User** -- handles email verification, user authentication, and password resets
- **Book** -- handles all book & user-specific book entry endpoints.
- **Errors** -- error handlers. Just basic 404 & 500 catching for now
- **Main** -- I'm still a bit unfamiliar with structuring Flask apps. The idea was to have a module for routes that don't require any authentication. Mostly, I didn't want to have my /index route hanging in src/ root directory.

### Required .flaskenv vars
- **SECRET_KEY**: this is *technically* optional since Config is gonna provide a default value, but it's a good idea to provide it so your key is kept secret.
- **DB_URI**: If in DEBUG, this is optional. App will just write to a local app.db file.

For verification emails, email logging, & library sharing
- **MAIL_SERVER**: (e.g. *smtp.googlemail.com*)
- **MAIL_PORT**: (e.g. 587)
- **MAIL_USE_TLS**: (leave empty if no)
- **MAIL_USERNAME**: \<your email login\>
- **MAIL_PASSWORD**: \<your email pw\>