from flask import Flask, render_template, url_for, g
import os
import sqlite3

from .db.threads import ThreadDB, Thread, Post
from .db.users import UserDB

app = Flask(__name__)

DATABASE_FILENAME = 'forum.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_FILENAME)

# class Users:
#     def __init__(self, db):
#         self.db = db
# 
#     def list_users(self):
#         return list(self.db.execute('select * from users;'))
# 
#     def username(self, user_id):
#         return self.db.execute('select username from users where user_id = ?',
#                 str(user_id)).fetchone()[0]
# 
# class Threads:
#     def __init__(self, db):
#         self.db = db
# 
#     def title(self, thread_id):
#         return self.db.execute('select title from threads where thread_id = ?',
#                 str(thread_id)).fetchone()[0]
# 
#     def list_threads(self):
#         return list(self.db.execute('select * from threads;'))
# 
#     def list_posts(self, thread_id):
#         return list(self.db.execute(
#                 'select * from posts where thread_id = ?', str(thread_id)))

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
