Flask OIDC Examples
-------------------

## Keycloak Local Server

Before running the application you need to create and configure a Keycloak local server.
You can start a local server using docker with:

```
docker run -d --name keycloak -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
```

Go to your browser and go to the URL: `http://localhost:8080`. Then login to the master keycloak realm using admin admin as the username and password.
Go to realms in the upper left and create a new realm called `myrealm`. Now, create
a user in `myrealm`. To do this click the `User` tab ont he left and set all the fields.
Note that the email just has to be a valid form of an email string (e.g., bherman@test.io).
After creating the user, click on the User and set a password by going to the `Credentials`
tab.

In order for the application to use keycloak you must create a Client in the realm. To do this, select `Client` on the left and give it a name called `flask` in this example. This is the client ID. Click `Next` and on the new screen turn on `Client authentication` and only have `Standard flow` selected for `Authentication flow` and click `Next`. On the next screen the only fields you need to enter are `Valid redirect URIs` and `Valid post logout redirect URIs`. They are as follows in this example:

- **Valid redirect URIs**: `http://localhost:8080/callback`
- **Valid post logout redirect URIs**: `http://localhost:8080/loggedOut`

Click `Next` to finish the process. Once finished you should be on the screen representing this new client. You can click on the `Credentials` tab to get the client secret which we will need to put in the Python files.

Keycloak should now be setup for use.

### Exposing Keycloak Group to Client

TODO

## Request-based Authlib Flask App

The Python file `request_flask_server.py` contains code for a Flask server that authenticates a user from Keycloak. Before running, open up the file and replace the `OAUTH2_CLIENT_ID` and the `OAUTH2_CLIENT_SECRET` to match your configuration from above.

You can start the server with:

```
python request_flask_server.py
```

You can go to the browser and go to the URL: `http://localhost:3000`. On that page there is a login button which when pressed, will redirect you to Keycloak to login as your user that you created. If successfully, Keycloak will redirect the browser back to the `callback` endpoint. The `callback` endpoint will reach back out to Keycloak on behalf of the user and get the user's information. This information for this example is put into a Flask session and displayed to the user. A logout button is then present on the screen. When clicked, the Flask session and Keycloak session will be destroyed and the user will go back to the original state of the homepage.

## Authlib Flask App

TODO
