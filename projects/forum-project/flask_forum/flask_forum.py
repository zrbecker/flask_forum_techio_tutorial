from flask import Flask, url_for
import os
import sqlite3

app = Flask(__name__)

DATABASE_FILENAME = 'forum.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_FILENAME)

@app.cli.command()
def initdb():
    """Initialize the database with the schema.sql query"""
    current_directory = os.path.dirname(__file__)
    init_script = os.path.join(current_directory, 'schema.sql')
    database_file = os.path.join(current_directory, 'forum.db')

    with sqlite3.connect(database_file) as conn:
        with open(init_script, 'r') as query:
            conn.executescript(query.read())

@app.cli.command()
def inittest():
    """Initializes the database with data from test_data.sql query"""
    current_directory = os.path.dirname(__file__)
    init_script = os.path.join(current_directory, 'test_data.sql')
    database_file = os.path.join(current_directory, 'forum.db')

    with sqlite3.connect(database_file) as conn:
        with open(init_script, 'r') as query:
            conn.executescript(query.read())

class Users:
    def __init__(self, db):
        self.db = db

    def list_users(self):
        return list(self.db.execute('select * from users;'))

class Threads:
    def __init__(self, db):
        self.db = db

    def list_threads(self):
        return list(self.db.execute('select * from threads;'))

    def list_posts(self, thread_id):
        return list(self.db.execute(
                'select * from posts where thread_id = ?', thread_id))

@app.route("/")
def index():
    db = sqlite3.connect(DATABASE_PATH)
    users = Users(db)
    return ', '.join(['{} {} {}'.format(user_id, username, password)
        for user_id, username, password in users.list_users()])

@app.route("/page")
def page():
    return '<a href="{}">back</a>'.format(url_for('index'))