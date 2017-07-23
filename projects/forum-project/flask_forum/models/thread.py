from ..flask_forum import db

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Thread {}>'.format(self.title)
