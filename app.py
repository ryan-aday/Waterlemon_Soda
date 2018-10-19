# title

from flask import Flask, request, render_template, \
                  flash, session, url_for, redirect
import story, os

app = Flask(__name__)

username = "admin"
password = "password"
app.secret_key = os.urandom(32)

@app.route("/")
def login():
    if username in session:
        return redirect(url_for("home"))
    return render_template("login.html");

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/auth")
def authenticate():
    if username == request.args["user"] and password == request.args["password"]:
        session[username] = username;
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/add")
def new_story():
    return render_template("add.html")

@app.route("/logout")
def logout():
    session.pop("admin")
    return redirect(url_for("login"))
# @app.route("/b")
# def b():
#     return
#
# @app.route("/c")
# def c():
#     return

app.debug = True;
app.run()

if __name__ == "__main__":
    app.debug = True;
    app.run()
