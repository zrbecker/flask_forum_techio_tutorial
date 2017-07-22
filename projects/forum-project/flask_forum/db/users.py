SQL_CREATE_USER = 'insert into users (username, password) values (?, ?)'
SQL_READ_USERNAME = 'select username from users where user_id = ?'
SQL_READ_PASSWORD = 'select password from users where user_id = ?'
SQL_READ_USER_ID_FROM_USERNAME = 'select user_id from users where username = ?'

class UserDB:
    def __init__(self, db):
        self.db = db

    def create_user(self, username, password):
        return self.db.execute(SQL_CREATE_USER, (username, password)).lastrowid

    def read_user_id(self, username):
        user_id, = self.db.execute(
                SQL_READ_USER_ID_FROM_USERNAME, (username,)).fetchone()
        return user_id

    def read_username(self, user_id):
        username, = self.db.execute(SQL_READ_USERNAME, (user_id,)).fetchone()
        return username

    def validate_password(self, user_id, password):
        db_password, = self.db.execute(SQL_READ_PASSWORD, (user_id,)).fetchone()
        return password == db_password
