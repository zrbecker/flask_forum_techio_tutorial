from .flask_forum import app
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

@app.cli.command()
def init_test_data():
    """Initializes the database with data from test_data.sql query"""
    current_directory = os.path.dirname(__file__)
    init_script = os.path.join(current_directory, 'test_data.sql')
    database_file = os.path.join(current_directory, 'forum.db')

    with sqlite3.connect(database_file) as conn:
        with open(init_script, 'r') as query:
            conn.executescript(query.read())
