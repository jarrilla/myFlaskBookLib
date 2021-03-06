## myFlaskBookLib

Basic Flask app emulating a personal library.

Registered users can add book entries to their library and add notes to any title in their virtual library.

### Setup
If setting up for first time, install requirements with:
> pip install -r requirements.txt

Then setup DB with:
> flask db upgrade

I also set up the following script to run in DEBUG mode

windows:
>\> ./bin/dev.ps1

This script assumes your venv is namved 'venv'


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
- **MAIL_USE_TLS**: leave empty if no
- **MAIL_USERNAME**: \<your email login\>
- **MAIL_PASSWORD**: \<your email pw\>

### Some other notes
* This is very basic, there isn't a single ounce of reactive components nor asynchronous render. Everything is re-rendered using POST/REDIRECT/GET
* I separated my /templates from /src since I like to keep my app logic separate from front end, though I saw a lot of flask apps online tend to put have /src/templates instead.
* I initially wanted to have a fully modular app in which each module would hold models, tests, etc.. but I couldn't figure out how to get Flask-Migrate to play along with that so I had to load all models from the root directory instead.
* Things this is missing:
  * Proper error handling without disrupting flow.
  * Password reset
  * Resend verification request
  * Edit your email address (in case you registered with a bogus one)
