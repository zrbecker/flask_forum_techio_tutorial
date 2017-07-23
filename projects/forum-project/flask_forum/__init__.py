from .flask_forum import app, db
from .models import User, Thread, Post
from datetime import datetime, timedelta

import os
import sqlite3

@app.cli.command()
def init_schema():
    """Initialize the database with the schema.sql query"""
    current_directory = os.path.dirname(__file__)
    init_script = os.path.join(current_directory, 'schema.sql')
    database_file = os.path.join(current_directory, 'forum.db')

    with sqlite3.connect(database_file) as conn:
        with open(init_script, 'r') as query:
            conn.executescript(query.read())

    db.drop_all()
    db.create_all()

@app.cli.command()
def init_test_data():
    """Initializes the database with data from test_data.sql query"""
    current_directory = os.path.dirname(__file__)
    init_script = os.path.join(current_directory, 'test_data.sql')
    database_file = os.path.join(current_directory, 'forum.db')

    with sqlite3.connect(database_file) as conn:
        with open(init_script, 'r') as query:
            conn.executescript(query.read())
    
    user1 = User('admin', 'test123')
    user2 = User('ralph', 'password123')

    thread1 = Thread('First Thread!')
    thread2 = Thread('Another Thread')

    now = datetime.utcnow() - timedelta(minutes=30)
    post1_time = now 
    post2_time = now + timedelta(minutes=1)
    post3_time = now + timedelta(minutes=5)

    post1 = Post(user1, thread1, 'First Post!', post1_time)
    post2 = Post(user2, thread1, 'Second post!', post2_time)
    post3 = Post(user2, thread2, 'Another post', post3_time)

    db.session.add(user1)
    db.session.add(user2)

    db.session.add(thread1)
    db.session.add(thread2)

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

    
