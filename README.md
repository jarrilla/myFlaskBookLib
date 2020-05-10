## myFlaskBookLib

Basic Flask app emulating a personal library.

Registered users can add book entries to their library and add notes to any title in their virtual library.


### To run in DEBUG mode
windows:
>$ ./bin/dev.ps1

### Required .flaskenv vars
- **SECRET_KEY**: this is *technically* optional since Config is gonna provide a default value, but it's a good idea to provide it so your key is kept secret.