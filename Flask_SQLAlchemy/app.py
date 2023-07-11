from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30))
    join_date = db.Column(db.DateTime)

    # def __repr__(self):
    #     return '<Member %r>' % self.username


# @app.route('/')
# def create_tables():
#     return 'Tables created successfully!'

with app.app_context():
    db.create_all()


Arsen = Members(username='Arsen', password='secret', email='Arsen@gmail.com', join_date='date.today()')
db.session.add(Arsen)
db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
