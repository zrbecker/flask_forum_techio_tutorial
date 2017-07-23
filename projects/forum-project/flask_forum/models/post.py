from datetime import datetime
from ..app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship('Thread',
            backref=db.backref('posts', lazy='dynamic'))
    message = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime)

    def __init__(self, user, thread, message, posted=None):
        self.user = user
        self.thread = thread
        self.message = message
        if posted is None:
            posted = datetime.utcnow()
        self.posted = posted

    def __repr__(self):
        return '<Post {}>'.format(self.message[:20])
