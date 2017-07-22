SQL_CREATE_USER = 'insert into users (username, password) values (?, ?)'
SQL_READ_USERNAME = 'select username from users where user_id = ?'
SQL_READ_PASSWORD = 'select password from users where user_id = ?'

class UserDB:
    def __init__(self, db):
        self.db = db

    def create_user(self, username, password):
        return self.db.execute(SQL_CREATE_USER, (username, password)).lastrowid

    def read_username(self, user_id):
        username, = self.db.execute(SQL_READ_USERNAME, (user_id,))
        return username

    def validate_password(self, user_id, password):
        db_password, = self.db.execute(SQL_READ_PASSWORD, (user_id,))
        return password == db_password
