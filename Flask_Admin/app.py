from os.path import dirname, join

from flask import Flask, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/admin_db'
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')
login_manager = LoginManager(app)
migrate = Migrate(app, db)

app.app_context().push()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(200))
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def __repr__(self):
        return '<Comment %r>' % self.id


class CommentView(ModelView):
    column_exclude_list = []
    create_modal = True
    # list_columns = ['comment_text', 'user_id']


class UserView(ModelView):
    column_display_pk = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='sha256')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You need to log in!!!!</h1>'


class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notyfi.html')


admin.add_view(UserView(User, db.session))
admin.add_view(CommentView(Comment, db.session))

admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))

path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))


# vzgo = User(username='Vazgen')
# db.session.add(vzgo)
# db.session.commit()

@app.route('/login')
def login():
    user = User.query.filter_by(id=1).first()
    login_user(user)
    return redirect(url_for('admin.index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
