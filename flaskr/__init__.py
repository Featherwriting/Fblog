import os
from  flask_babel import Babel
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskext.markdown import Markdown
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__, instance_relative_config=True)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
admin = Admin(app, name="microblog")
db = SQLAlchemy(app)
babel=Babel()
babel.init_app(app)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.Text)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    chat_list = db.Column(db.JSON)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    content = db.Column(db.Text())
    time = db.Column(db.DateTime(), default=datetime.datetime.now)



app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
)
md = Markdown(app,
            extensions=['footnotes'],
            entension_configs={'footnotes':('PLACE_MARKER', '```')},
            safe_mode=True,
            output_format='html4')


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Comment, db.session))


from flaskr import blog, chat, auth

@app.route("/hello")
def hello():
    with app.app_context():
        db.create_all()
    return "Hello, World!"