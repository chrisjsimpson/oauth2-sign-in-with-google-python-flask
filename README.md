# OAuth Google Signin Example

Simple OAuth 'Sign in with Google' oauth flow. 

- Without 0auth, okta, firebase. Just plain old python


# Install

Create an oauth client in https://console.developers.google.com/apis/credentials to
get your client_id and client secret. You'll also need to set the allowed return_uri to 
the same as in .env.example

```
virtualenv venv
. venv/bin/activate
pip instal -r requirements.txt
cp .env.example .env
```

Update .env with your settings

# Run

```
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

Visit http://127.0.0.1:5000

Click 'Signin' and you'll be directed to google, 
then you're be redirected to show your profile information.
