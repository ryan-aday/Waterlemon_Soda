# title

from flask import Flask, request, render_template,
                  flash, session, url_for, redirect
import sqlite3

app = Flask(__name__)

username = "admin"
password = "password"

@app.route("/")
def login():
    return render_template("login.html");

@app.route("/register")
def register():
    return render_template("register.html")

# @app.route("/home")

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
