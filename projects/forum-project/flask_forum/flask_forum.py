from flask import Flask, render_template, url_for, g
import os
import sqlite3

from .db.threads import ThreadDB, Thread, Post
from .db.users import UserDB

app = Flask(__name__)

DATABASE_FILENAME = 'forum.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_FILENAME)

@app.route('/')
def index():
    return threads() 

@app.route('/threads')
def threads():
    db = sqlite3.connect(DATABASE_PATH)
    thread_db = ThreadDB(db)
    threads = thread_db.list_threads()
    return render_template('threads.html', threads=threads)

@app.route('/posts/<thread_id>')
def posts(thread_id):
    db = sqlite3.connect(DATABASE_PATH)
    thread_db = ThreadDB(db)
    user_db = UserDB(db)

    thread = thread_db.read_thread(thread_id)
    posts = thread_db.list_posts_for_thread(thread_id)

    posts = [
        {
            'username': user_db.read_username(post.user_id),
            'message': post.message
        }
        for post in posts]
    return render_template('posts.html', posts=posts, title=thread.title)
