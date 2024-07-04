"""Python Flask WebApp OAuth 2.0 Authorization code flow example using Requests
"""

import json
from urllib.parse import quote_plus, urlencode

import requests
from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import jwt
from flask import Flask, abort, redirect, render_template, request, session, url_for

appConf = {
    "OAUTH2_CLIENT_ID": "flask",
    "OAUTH2_CLIENT_SECRET": "2Af6AeAK29YBzA9CuRRzmUhD5zaFdyjI",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myrealm",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 3000
}

app = Flask(__name__)
app.secret_key = appConf.get("FLASK_SECRET")

discovery = requests.get(appConf.get("OAUTH2_ISSUER") + "/.well-known/openid-configuration").json()

client = OAuth2Session(
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    scope="openid profile email",
    redirect_uri="http://localhost:3000/callback",
)

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback")
def callback():
    token_endpoint = discovery["token_endpoint"]
    token = client.fetch_token(token_endpoint, authorization_response=request.url)
    certs = requests.get(appConf.get("OAUTH2_ISSUER") + "/protocol/openid-connect/certs")
    access = jwt.decode(token['access_token'], certs.json())
    id = jwt.decode(token['id_token'], certs.json())
    userinfo_endpoint = discovery["userinfo_endpoint"]
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    user_info = requests.get(userinfo_endpoint, headers=headers)
    session["user"] = {}
    session["user"]["access"] = access
    session["user"]["id"] = id
    session["user"]["token"] = token
    session["user"]["userinfo"] = user_info.json()
    return redirect(url_for("home"))


@app.route("/login")
def login():
    session.pop("user", None)
    if "user" in session:
        abort(404)
    authurl = client.create_authorization_url(discovery["authorization_endpoint"])
    return redirect(authurl[0])


@app.route("/loggedout")
def loggedOut():
    if "user" in session:
        abort(404)
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    id_token = session["user"]["token"]["id_token"]
    session.clear()
    return redirect(
        discovery["end_session_endpoint"]
        + "?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("loggedOut", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConf.get("FLASK_PORT", 3000), debug=True)
"""Python Flask WebApp OAuth 2.0 Authorization code flow example
"""
