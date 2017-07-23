from flask import Flask, redirect, request, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'development secret'

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flask_forum.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)

from .models import User, Post, Thread

@app.route('/')
def index():
    return threads() 

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('register.html')

        username = request.form.get('username')
        password = request.form.get('password')
        if username is not None and password is not None:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['username'] = new_user.username
    except Exception as e:
        print('Register Exception:', e)

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    try:
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if password == user.password:
                session['user_id'] = user.id
                session['username'] = user.username
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
    context = {
        'threads': [],
        'username': session.get('username', None)
    }

    threads = Thread.query.all()
    for thread in threads:
        first_post = thread.posts.order_by(Post.posted.asc()).first()
        last_post = thread.posts.order_by(Post.posted.desc()).first()
        context['threads'].append({
            'thread_id': thread.id,
            'title': thread.title,
            'author': first_post.user.username,
            'created_time': first_post.posted.strftime('%c'),
            'last': last_post.user.username,
            'last_post_time': last_post.posted.strftime('%c')
        })

    return render_template('threads.html', **context)

@app.route('/thread/create', methods=['GET', 'POST'])
def thread_create():
    username = session.get('username', None)
    if username is None:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('new_thread.html', username=username)

    if 'thread-title' in request.form and 'thread-message' in request.form:
        user_id = session['user_id']
        title = request.form['thread-title']
        message = request.form['thread-message']

        user = User.query.filter_by(id=user_id).first()
        new_thread = Thread(title)
        new_post = Post(user, new_thread, message)

        db.session.add(new_thread)
        db.session.add(new_post)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/thread/<thread_id>/post/create', methods=['GET', 'POST'])
def post_create(thread_id):
    username = session.get('username', None)
    if username is None:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('new_post.html',
            username=username, thread_id=thread_id)

    if 'thread-message' in request.form:
        user_id = session['user_id']
        message = request.form['thread-message']

        user = User.query.filter_by(id=user_id).first()
        thread = Thread.query.filter_by(id=thread_id).first()
        new_post = Post(user, thread, message)

        db.session.add(new_post)
        db.session.commit()

    return redirect(url_for('posts', thread_id=thread_id))

@app.route('/posts/<thread_id>')
def posts(thread_id):
    thread = Thread.query.filter_by(id=thread_id).first()
    context = {
        'posts': [],
        'title': thread.title,
        'username': session.get('username', None),
        'thread_id': thread_id
    }

    for post in thread.posts:
        context['posts'].append({
            'username': post.user.username,
            'message': post.message
        })

    return render_template('posts.html', **context)
