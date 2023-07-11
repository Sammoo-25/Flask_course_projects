from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30))

    orders = db.relationship('Order', backref='user', lazy='dynamic')
    courses = db.relationship('Courses', secondary='user_courses', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<User: %r>' % self.username

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

db.Table('user_courses',
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
         db.Column('course_id', db.Integer, db.ForeignKey('courses.id')))







@app.route('/regis', methods=['POST', 'GET'])
def registor():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['psw']
        if username and email and password:
            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        return render_template('index.html')
    else:
        return render_template('index.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
