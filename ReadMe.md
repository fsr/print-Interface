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
gunicorn app:app -b '0.0.0.0'
```

The System is also currently working without sessions, so if one user changes something, everyone can see it.
