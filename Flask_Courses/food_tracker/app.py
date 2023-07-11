import os.path

import psycopg2
from flask import Flask, render_template, request

create_path = os.path.dirname(__file__)

app = Flask(__name__, template_folder=f'{create_path}/static')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Samvel357552@localhost:5432/market_db'

# Database configuration
db_host = 'localhost'
db_port = '5432'
db_name = 'market_db'
db_user = 'postgres'
db_password = 'Samvel357552'

# Establish a database connection
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['food_date']

        cursor = conn.cursor()
        insert_query = "INSERT INTO dates (dates) VALUES (%s)"
        cursor.execute(insert_query, [str(date), ])
        conn.commit()
        cursor.close()

        cursor = conn.cursor()
        select_query = "SELECT dates FROM dates order by dates desc"
        cursor.execute(select_query)
        added_dates = cursor.fetchall()
        cursor.close()

        return render_template('index.html', added_dates=added_dates)

    # cursor = conn.cursor()
    # select_query = "SELECT dates FROM dates"
    # cursor.execute(select_query)
    # existing_date = cursor.fetchall()
    # cursor.close()
    return render_template('index.html', existing_date=None)


@app.route('/day', methods=['GET', 'POST'])
def day():
    if request.method == 'POST':
        selected_food = request.form['select_food']
        return render_template('day.html', selected_food=selected_food)

    cursor = conn.cursor()
    select_query = "SELECT food_name FROM foods"
    cursor.execute(select_query)
    added_foods_name = cursor.fetchall()
    cursor.close()

    return render_template('day.html', added_foods_name=added_foods_name)


@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        food_name = request.form['food-name']
        calories = request.form['calo-name']
        meal_type = request.form['meal-name']

        # Insert the data into the database
        cursor = conn.cursor()
        insert_query = "INSERT INTO foods (food_name, calories, meal_type) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (food_name, calories, meal_type))
        conn.commit()
        cursor.close()

        # Retrieve the added foods from the database
        cursor = conn.cursor()
        select_query = "SELECT food_name, calories, meal_type FROM foods"
        cursor.execute(select_query)
        added_foods = cursor.fetchall()
        cursor.close()

        return render_template('food.html', added_foods=added_foods)

    # Fetch the existing foods from the database
    cursor = conn.cursor()
    select_query = "SELECT food_name, calories, meal_type FROM foods"
    cursor.execute(select_query)
    existing_foods = cursor.fetchall()
    cursor.close()

    return render_template('food.html', added_foods=existing_foods)


if __name__ == '__main__':
    app.run(debug=True)
