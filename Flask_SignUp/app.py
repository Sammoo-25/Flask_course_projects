from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Length, Regexp, Email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Mysecret!'

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeriS4nAAAAACm-6oIe7te8PiN-0YKtuw_eh1W-'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeriS4nAAAAAPRo0pg39pjVdT-Flc4sp5AMBO7S'

db = SQLAlchemy(app)


class SighnUp(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(message='Username is required'),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters'),
        Regexp(r'^\w+$', message='Username can only contain letters, numbers, and underscores')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')])
    email = StringField('Email', validators=[Email()])
    birth_day = DateField('Birth Day')

    recaptcha = RecaptchaField()


class Signin(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(message='Username is required'),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters'),
        Regexp(r'^\w+$', message='Username can only contain letters, numbers, and underscores')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')])


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/regis', methods=['POST', 'GET'])
def registor():
    form = SighnUp()
    signIn = Signin()
    from models import Users
    if form.validate_on_submit():
        if form.username.data and form.email.data and form.password.data and form.birth_day.data:
            new_user = Users(username=form.username.data, email=form.email.data, password=form.password.data,
                 birth_day=form.birth_day.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signin'))

    return render_template('index.html', form=form, signIn=signIn)


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    from models import Users
    signIn = Signin()
    if signIn.validate_on_submit():
        user = Users.query.filter_by(username=signIn.username.data).first()
        if user and user.password == signIn.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "error")

    return render_template('signin.html', signIn=signIn)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
