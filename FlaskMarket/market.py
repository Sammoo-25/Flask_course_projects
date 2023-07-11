# from urllib import request

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# db = SQLAlchemy(app)

# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False, unique=True)
#     barcode = db.Column(db.String(length=30), nullable=False, unique=True)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)
#
# with app.app_context():
#     db.create_all()
#
#
# with app.app_context():
#     item1 = Item(name='Item 1', price=10, barcode='12345', description='Description 1')
#     item2 = Item(name='Item 2', price=20, barcode='67890', description='Description 2')
#
#     db.session.add(item1)
#     db.session.add(item2)
#     db.session.commit()


@app.route('/')
def index():
    return "Is this working?"


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html', items=items)


@app.route('/base')
def base():
    return render_template('basic_templates.html')


if __name__ == '__main__':
    app.run(debug=True)
