SQL_LIST_THREADS = 'select thread_id, title from threads'
SQL_LIST_POSTS_FOR_THREAD = 'select post_id, user_id, message from posts' \
        ' where thread_id = ? ORDER BY posted'
SQL_LIST_POSTS_FOR_USER = 'select thread_id, user_id, message from posts' \
        ' where post_id = ? ORDER BY posted'

SQL_READ_THREAD = 'select title from threads where thread_id = ?'

SQL_READ_THREAD_AUTHOR_USER_ID = 'select user_id, posted from posts' \
        ' where thread_id = ? order by posted limit 1'
SQL_READ_THREAD_LAST_USER_ID = 'select user_id, posted from posts' \
        ' where thread_id = ? order by posted desc limit 1'

SQL_CREATE_THREAD = 'insert into threads (title) values (?)'
SQL_CREATE_POST = 'insert into posts (user_id, thread_id, message)' \
        ' values (?, ?, ?)'

class Thread:
    def __init__(self, thread_id, title):
        self.thread_id = thread_id
        self.title = title

class Post:
    def __init__(self, post_id, user_id, thread_id, message):
        self.post_id = post_id
        self.user_id = user_id
        self.thread_id = thread_id
        self.message = message

class ThreadDB:
    def __init__(self, db):
        self.db = db

    def list_threads(self):
        return [Thread(thread_id, title)
                for thread_id, title in self.db.execute(SQL_LIST_THREADS)]

    def list_posts_for_thread(self, thread_id):
        return [Post(post_id, user_id, thread_id, message)
                for post_id, user_id, message
                in self.db.execute(SQL_LIST_POSTS_FOR_THREAD, (thread_id,))]

    def list_posts_for_user(self, user_id):
        return [Post(post_id, user_id, thread_id, message)
                for post_id, thread_id, message
                in self.db.execute(SQL_LIST_POSTS_FOR_USER, (user_id,))]

    def read_thread(self, thread_id):
        title, = self.db.execute(SQL_READ_THREAD, (thread_id,)).fetchone()
        return Thread(thread_id, title)

    def read_thread_author_id(self, thread_id):
        user_id, posted = self.db.execute(SQL_READ_THREAD_AUTHOR_USER_ID,
                (thread_id,)).fetchone()
        return user_id, posted

    def read_thread_last_id(self, thread_id):
        user_id, posted = self.db.execute(SQL_READ_THREAD_LAST_USER_ID,
                (thread_id,)).fetchone()
        return user_id, posted

    def create_thread(self, user_id, title, message):
        thread_id = self.db.execute(SQL_CREATE_THREAD, (title,)).lastrowid
        self.create_post(user_id, thread_id, message)

    def create_post(self, user_id, thread_id, message):
        self.db.execute(SQL_CREATE_POST, (user_id, thread_id, message))
        self.db.commit()
