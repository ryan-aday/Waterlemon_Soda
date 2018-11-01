#Waterlemon_Soda (Joyce Liao, Kendrick Liang, Kenny Li, Johnson Li)
#SoftDev pd8
#P#00: Da art of Storytellin'
#2018-10-29


from flask import Flask, request, render_template, \
                  flash, session, url_for, redirect
from util import story
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)


#---------- Login Routes ----------
#Sends the user to the login page if they are logged in
#If not they have to login or register
@app.route("/", methods = ["GET"])
def login():
    if "logged_in" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

#Authenticates user and creates a session
@app.route("/auth", methods = ["POST"])
def authenticate():
    if story.auth_user(request.form["user"], request.form["password"]):
        session["logged_in"] = request.form["user"]
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

#---------- Register Routes ----------
#Sends the user to the register page to create account
@app.route("/register", methods = ["GET"])
def register():
    return render_template("register.html")

#Adds user to the database after they register
#Flashes message accordingly if user exists or form isn't filled
@app.route("/adduser", methods = ["POST"])
def add_user():
    if(not request.form["user"].strip() or not request.form["password"] or not request.form["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(story.check_user(request.form["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.form["password"] != request.form["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    story.add_user(request.form["user"], request.form["password"])
    session["logged_in"] = request.form["user"]
    return redirect(url_for("home"))

#---------- Home Route ----------
#Displays home page
@app.route("/home", methods = ["GET"])
def home():
    return render_template("home.html", user=session["logged_in"], stories = story.get_stories(session["logged_in"]))


#---------- Adding New Stories ----------
#Displays page for adding stories
@app.route("/add", methods = ["POST"])
def new_story():
    return render_template("add.html")

#Adds new story to the database
#Flashes messages accordingly if form isn't filled
@app.route("/newstory", methods = ["POST"])
def newstory():
    if(not request.form["story_title"].strip() or not request.form["story_content"].strip()):
        flash("please fill in all fields")
        return redirect(url_for("new_story"), code=307)
    flash("story has been added!")
    story.add_story(request.form["story_title"], request.form["story_content"], session["logged_in"])
    return redirect(url_for("home"))

#---------- Editing Existing Stories ----------
#Sends user to to the edit page to fill out form for new entry
@app.route("/edit", methods = ["POST"])
def edit_story():
    story_id = request.form["sid"]
    info = story.get_last_entry(story_id)
    return render_template("edit.html", story_title = info[0], last_entry= info[1], sid = story_id)

#Adds new entry to the database
#Flashes messages accordingly if form isn't filled
@app.route("/editstory", methods = ["POST"])
def new_entry():
    if(not request.form["new_entry"].strip()):
        flash("Please fill in an entry")
        return redirect(url_for("edit_story", sid=request.form["sid"]), code=307)
    flash("Entry has been added! You can now view the story.")
    story.add_new_entry(request.form["sid"], request.form["new_entry"], session["logged_in"])
    return redirect(url_for("home"))

#---------- Viewing Existing Stories ----------
#Displays story with all of its entries
@app.route("/view", methods = ["POST"])
def view_story():
    title = story.get_story_name(request.form["sid"])
    entries = story.get_story_entries(request.form["sid"])
    return render_template("view.html", story_title = title, author = entries[0][2], list = entries)

#---------- Logout Route ----------
#Logs the user out and removes session
@app.route("/logout", methods = ["POST"])
def logout():
    session.pop("logged_in")
    return redirect(url_for("login"))

app.debug = True
app.run()

if __name__ == "__main__":
    app.debug = True
    app.run()
