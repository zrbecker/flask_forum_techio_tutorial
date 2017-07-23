from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'development secret'

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flask_forum.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
