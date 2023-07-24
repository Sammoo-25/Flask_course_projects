from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/API_db'
db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

app.app_context().push()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#
# vzgo = Users(username='Vazgen')
# db.session.add(vzgo)
# db.session.commit()

# it2 = Item(name='Item_2', user_id=1)
# db.session.add(it2)
# db.session.commit()


manager.create_api(Users, methods=['GET', 'POST'])
manager.create_api(Item, methods=['GET', 'POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
