from flask import Flask, render_template, redirect, request, session, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

# See https://developers.google.com/identity/protocols/oauth2/web-server#httprest_1 # noqa

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12)
app.config.update(os.environ)

client_id = app.config["CLIENT_ID"]
client_secret = app.config["CLIENT_SECRET"]
redirect_uri = app.config["REDIRECT_URI"]
response_type = app.config["RESPONSE_TYPE"]
scope = app.config["SCOPE"]


@app.route("/")
def signin():
    return render_template("signin.html")


@app.route("/withgoogle")
def google():

    state = str(os.urandom(12))
    session["state"] = state

    redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?scope={scope}&\
access_type=offline&\
include_granted_scopes=true&\
response_type=code&\
state={state}&\
redirect_uri={redirect_uri}&\
client_id={client_id}"
    return redirect(redirect_url)


@app.route("/google-oauth2callback/")
def google_return():
    # Verify state token
    if request.args["state"] != session["state"]:
        return "Invalid state token", 403

    # From the returned url, exchange authorization code for an access token
    authorization_code = request.args.get("code", None)

    if authorization_code is None:
        return "Error: Google did not give authorization_code"

    # Get an access token by calling https://oauth2.googleapis.com/token,
    # passing the authorization_code.
    data = {
        "code": authorization_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    resp = requests.post("https://oauth2.googleapis.com/token", data=data)

    # Try and get access token from the response
    access_token = resp.json().get("access_token", None)
    refresh_token = resp.json().get("refresh_token", None)
    scope = resp.json().get("scope", None)
    token_type = resp.json().get("token_type", None)

    # Put access token and refresh_token in session (normally would store in database) # noqa
    session["access_token"] = access_token
    session["refresh_token"] = refresh_token
    session["scope"] = scope
    session["token_type"] = token_type

    return redirect(url_for("logged_in"))


@app.route("/loggedin")
def logged_in():

    # Get user profile information (name, email)
    headers = {"Authorization": "Bearer " + session["access_token"]}
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
        headers=headers,  # noqa
    )

    return render_template("logged-in.html", data=resp.json())
