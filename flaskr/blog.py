from flask import render_template, request, flash, redirect, url_for, g
from flaskr import app, Article, Comment,User

#from flaskr.auth import login_required
from flaskr import db
import functools

from flaskr.auth import login_required


@app.route('/')
@app.route('/home')
def home():
    posts = Article.query.all()
    return render_template('list.html', title="Home", posts=posts)


@app.route('/post/<int:id>', methods=('GET', 'POST'))
def article(id):
    if request.method == 'POST':
        error = None
        print(g.user)
        if g.user is None:
            print("yesy")
            error = '请先登录才可以发表评论'
        if request.form['content'] == '':
            error = '评论不能为空'


        if error is None:
            new_comment = Comment(article_id=id, content=request.form['content'], author_id=g.user.id)
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash(error)
    post = Article.query.get(id)
    comments = Comment.query.filter(Comment.article_id == id).all()
    return render_template('article.html', title="Post", post=post, comments=comments, user=g.user)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        author_id = g.user.username
        title = request.form['title']
        body = request.form['body']
        new_article = Article(author_id = author_id, title = title, content =body)

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

