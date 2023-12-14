# Email to Print System

## Requirements

1. python with flask
2. lpr installed on system (should be by default)
3. an email account

## Operating

create an .env file in the repo with the following variables:
```
USERNAME=<the username of the account>
PASSWORD=<password of the account>
```

then run
```
python3 app.py
```
or 
```
flask run --host=0.0.0.0
```

THIS IS CURRENTLY ONLY THE TEST SERVER.

The System is also currently working without sessions, so if one user changes something, everyone can see it.