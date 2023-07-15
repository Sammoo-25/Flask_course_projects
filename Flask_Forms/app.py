from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret!'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message='Username is required'),
        Length(min=4, max=20, message='Username must be between 4 and 20 characters'),
        Regexp(r'^\w+$', message='Username can only contain letters, numbers, and underscores')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')])
    age = IntegerField('Age')
    email = StringField('Email')


# class User:
#     def __init__(self, username, age, email):
#         self.username = username
#         self.age = age
#         self.email = email


@app.route('/', methods=['POST', 'GET'])
def index():
    # myuser = User('Karlenchik', 34, 'Karlencho@gmail.com')
    form = LoginForm()

    if form.validate_on_submit():
        return f'<h1>Username: {form.username.data} Password: {form.password.data} Age: {form.age.data} Email:{form.email.data}</h1>'

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
