from flask import Flask, redirect, request, render_template, session, url_for
import os
import sqlite3

from .db.threads import ThreadDB, Thread, Post
from .db.users import UserDB

app = Flask(__name__)
app.secret_key = 'development secret'

DATABASE_FILENAME = 'forum.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_FILENAME)

@app.route('/')
def index():
    return threads() 

@app.route('/login', methods=['POST'])
def login():
    try:
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            db = sqlite3.connect(DATABASE_PATH)
            user_db = UserDB(db)

            user_id = user_db.read_user_id(username)
            if user_db.validate_password(user_id, password):
                session['user_id'] = user_id
                session['username'] = username
    except Exception as e:
        print('Login Exception:', e)

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    if 'user_id' in session:
        del session['user_id']

    return redirect(url_for('index'))

@app.route('/threads')
def threads():
    db = sqlite3.connect(DATABASE_PATH)
    thread_db = ThreadDB(db)
    user_db = UserDB(db)

    threads = thread_db.list_threads()
    thread_contexts = []
    for thread in threads:
        thread_id = thread.thread_id
        author_id, created_time = thread_db.read_thread_author_id(thread_id)
        last_id, last_post_time = thread_db.read_thread_last_id(thread_id)
        thread_context = {
            'thread_id': thread_id,
            'title': thread.title,
            'author': user_db.read_username(author_id),
            'created_time': created_time,
            'last': user_db.read_username(last_id),
            'last_post_time': last_post_time
        }
        thread_contexts.append(thread_context)

    username = None
    if 'username' in session:
        username = session['username']
    return render_template('threads.html', threads=thread_contexts,
            username=username)

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
        for post in posts
    ]

    username = None
    if 'username' in session:
        username = session['username']
    return render_template('posts.html', posts=posts, title=thread.title,
            username=username)
