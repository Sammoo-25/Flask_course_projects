from flask import Flask, render_template, request, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, \
    fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/login_db'

app.app_context().push()
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)

# login_manager.login_message = 'You need to login first !!!'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = Users.query.filter_by(username=username).first()

        if not user:
            return '<h1>User does not exist!</h1>'

        login_user(user, remember=True)

        if 'next' in session:
            next = session['next']

            if next is not None:
                return redirect(next)

        return '<h1>You are noe logged in!!</h1>'

    session['next'] = request.args.get('next')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return f'<h1>You Logged Out!!</h1>'


@app.route('/home')
@login_required
def home():
    return f'<h1>You are in the protected area!! {current_user.username}</h1>'


@app.route('/fresh')
@fresh_login_required
def fresh():
    return '<h1>You have a fresh session!!</h1>'


# arsen = Users(username='Arsencho')
# db.session.add(arsen)
# db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
