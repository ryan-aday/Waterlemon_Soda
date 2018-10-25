# title

from flask import Flask, request, render_template, \
                  flash, session, url_for, redirect
from util import story
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route("/")
def login():
    if "logged_in" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/adduser")
def add_user():
    if(story.check_user(request.args["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.args["password"] != request.args["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    story.add_user(request.args["user"], request.args["password"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))

@app.route("/auth")
def authenticate():
    # if username = request.args["user"] and password = request.args["password"]:
    if story.auth_user(request.args["user"], request.args["password"]):
        session["logged_in"] = request.args["user"]
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

@app.route("/home")
def home():
    return render_template("home.html", user=session["logged_in"], stories = story.get_stories(session["logged_in"]))

@app.route("/add")
def new_story():
    return render_template("add.html")

@app.route("/newstory")
def newstory():
    flash("story has been added!")
    story.add_story(request.args["story_title"], request.args["story_content"], session["logged_in"])
    return redirect(url_for("home"))

@app.route("/view")
def view_story():
    title = story.get_story_name(request.args["sid"])
    entries = story.get_story_entries(request.args["sid"])
    return render_template("view.html", story_title = title, author = entries[0][2], list = entries)

@app.route("/edit")
def edit_story():
    story_id = request.args["sid"]
    info = story.get_last_entry(story_id)
    return render_template("edit.html", story_title = info[0], last_entry= info[1], sid = story_id)

@app.route("/editstory")
def new_entry():
    story.add_new_entry(request.args["sid"], request.args["new_entry"], session["logged_in"])
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("login"))

app.debug = True
app.run()

if __name__ == "__main__":
    app.debug = True
    app.run()
