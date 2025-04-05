from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
import bcrypt
import Data_handler as sanitiser


# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        # sanitise feedback to prevent cross sight scripting
        feedback = sanitiser.make_web_safe(feedback)
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        username = sanitiser.make_web_safe(username)
        password = request.form["password"]
        DoB = request.form["dob"]

        try:
            password = sanitiser.check_password(password)  # Validate password
            encoded_password = password  # Already encoded in check_password()
        except ValueError:
            # if error is returned go back to sign up page
            return render_template("/signup.html")
        else:
            # salt to add to password before hashing
            salt = bcrypt.gensalt()
            # create hashed password
            hashed_password = bcrypt.hashpw(password=encoded_password, salt=salt)
            # add user into database
            dbHandler.insertUser(username, hashed_password, DoB, salt)
            return render_template("/index.html")

    else:

        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        # Retrieve the stored salt value for this username from the database
        salt = dbHandler.retrieveSalt(username)
        # Encode the password string into bytes (required for hashing)
        encoded_password = password.encode()
        # Hash the encoded password using bcrypt and the retrieved salt
        hashed_password = bcrypt.hashpw(password=encoded_password, salt=salt)
        # Check if the username and hashed password match an existing user in the database
        isLoggedIn = dbHandler.retrieveUsers(username, hashed_password)
        # If the user is authenticated successfully
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=8080)
