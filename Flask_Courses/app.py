import json
import os.path

import psycopg2
from flask import Flask, jsonify, request, url_for, redirect, render_template

create_path = os.path.dirname(__file__)

app = Flask(__name__, template_folder=f'{create_path}/template')

app.config['SECRET_KEY'] = 'Thisissecret!!'

# POSTGRES_HOST = '127.0.0.1'
# POSTGRES_PORT = '5432'
# POSTGRES_DB = 'market_db'
# POSTGRES_USER = 'postgres'
# POSTGRES_PASSWORD = 'Samvel357552'
#
# def create_connection():
#     connection = psycopg2.connect(
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT,
#         database=POSTGRES_DB,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD
#     )
#     return connection
#
# @app.route('/create_and_insert')
# def create_and_insert():
#     # Create connection
#     connection = create_connection()
#
#     # Create a cursor
#     cursor = connection.cursor()
#
#     # Create a table
#     create_table_query = '''
#         CREATE TABLE IF NOT EXISTS example (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(50),
#             age INTEGER
#         );
#     '''
#     cursor.execute(create_table_query)
#
#     # Insert data into the table
#     insert_query = '''
#         INSERT INTO example (name, age) VALUES ('John Doe', 30);
#     '''
#     cursor.execute(insert_query)
#
#     # Commit the changes
#     connection.commit()
#
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()
#
#     return 'Data created and inserted successfully!'



@app.route('/')
def index():
    print(create_path)
    return '<h1>World</h1>'



@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    with open('questions.json') as f:
        data = json.load(f)
    return render_template('home.html', name=name, display=False, dict=data)
    # return f'<h1>Hello, {name} You are on the home page!! </h1>'


@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template("forms.html")
    else:
        name = request.form['name']
        # location = request.form['location']
        # return f'Hello, my name is {name}, I am from {location}'
        return redirect(url_for('home', name=name))


# @app.route('/process', methods=['POST'])
# def process():
#     name = request.form['name']
#     location = request.form['location']
#
#     return f'Hello, my name is {name}, I am from {location}'


@app.route('/json', methods=['GET', 'POST'])
def json_route():
    with open('questions.json') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
