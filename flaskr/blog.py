from flask import render_template, request, flash, redirect, url_for, g
from flaskr import app, Article, Comment,User

#from flaskr.auth import login_required
from flaskr import db
import functools

from flaskr.auth import login_required, creator_required


@app.route('/')
@app.route('/home')
def home():
    posts = Article.query.all()
    return render_template('list.html', title="Home", posts=posts)


@app.route('/post/<int:id>', methods=('GET', 'POST'))
def article(id):
    if request.method == 'POST':
        error = None
        if g.user is None:
            error = '请先登录才可以发表评论'
        if request.form['content'] == '':
            error = '评论不能为空'


        if error is None:
            username = User.query.get(g.user.id).username
            new_comment = Comment(article_id=id, content=request.form['content'], author_id=g.user.id, username=username)
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash(error)
    post = Article.query.get(id)
    comments = Comment.query.filter(Comment.article_id == id).all()
    alluser = User.query.all()
    return render_template('article.html', title="Post", post=post, comments=comments, user=g.user, alluser = alluser)

@app.route('/create', methods=('GET', 'POST'))
@login_required
@creator_required
def create():
    if request.method == 'POST':
        author_id = g.user.username
        title = request.form['title']
        body = request.form.get('body')
        summary = request.form['sum']
        new_article = Article(author_id = author_id, title = title, content =body, summary = summary)

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.session.add(new_article)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('create.html')

