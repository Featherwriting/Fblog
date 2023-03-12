import functools

from flask import render_template, request, flash, redirect, url_for, session, g, before_render_template
from flaskr import app, Article, User
from sqlalchemy import exists
from flaskr import db

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            username_exists = db.session.query(
                exists().where( User.username == username )
            ).scalar()
            if (username_exists):
                user_now = User.query.filter(User.username == username).first()
                if(user_now.check_password(password)):
                    session.clear()
                    session['user_id'] = user_now.id
                    return redirect('/home')
                else:
                    error = 'Incorrect password'
            else:
                error = 'Incorrect username'
        if not error is None: flash(error)


    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.route('/reg', methods=('GET', 'POST'))
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            username_exists = db.session.query(
                exists().where(User.username == username)
            ).scalar()
            if (not username_exists):
                new_user = User(username = username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                return redirect('login.html')
            else:
                error = '用户名已存在'

        if not error is None: flash(error)


    return render_template('reg.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')