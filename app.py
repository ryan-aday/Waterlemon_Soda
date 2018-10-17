# title

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return

@app.route("/a")
def a():
    return

@app.route("/b")
def b():
    return

@app.route("/c")
def c():
    return

app.debug = True;
app.run()

if __name__ == "__main__":
    app.debug = True;
    app.run()
