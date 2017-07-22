from flask import Flask, render_template, url_for
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

    def username(self, user_id):
        return self.db.execute('select username from users where user_id = ?',
                str(user_id)).fetchone()[0]

class Threads:
    def __init__(self, db):
        self.db = db

    def title(self, thread_id):
        return self.db.execute('select title from threads where thread_id = ?',
                str(thread_id)).fetchone()[0]

    def list_threads(self):
        return list(self.db.execute('select * from threads;'))

    def list_posts(self, thread_id):
        return list(self.db.execute(
                'select * from posts where thread_id = ?', str(thread_id)))

@app.route('/')
def index():
    return threads() 

@app.route('/threads')
def threads():
    db = sqlite3.connect(DATABASE_PATH)
    threads = [{'thread_id': thread_id, 'title': title}
            for thread_id, title in Threads(db).list_threads()]
    return render_template('threads.html', threads=threads)

@app.route('/posts/<thread_id>')
def posts(thread_id):
    db = sqlite3.connect(DATABASE_PATH)
    threaddb = Threads(db)
    title = threaddb.title(thread_id)
    posts = threaddb.list_posts(thread_id)
    usersdb = Users(db)
    posts = [{'username': usersdb.username(user_id), 'message': message}
            for _, user_id, _, message in posts]
    return render_template('posts.html', posts=posts, title=title)

@app.route("/page")
def page():
    return '<a href="{}">back</a>'.format(url_for('index'))