from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello Flask! <a href="{}">page</a>'.format(url_for('page'))

@app.route("/page")
def page():
    return '<a href="{}">back</a>'.format(url_for('index'))