import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'
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


@app.route('/member', methods=['GET'])
def get_members():
    cursor = conn.cursor()
    select_query = "SELECT id, name, email, level FROM members"
    cursor.execute(select_query)
    all_members = cursor.fetchall()
    cursor.close()

    return_value = []

    for member in all_members:
        member_dict = {}
        member_dict['id'] = member[0]
        member_dict['name'] = member[1]
        member_dict['email'] = member[2]
        member_dict['level'] = member[3]

        return_value.append(member_dict)

    username = request.authorization.username
    password = request.authorization.password

    return jsonify({'members': return_value, 'username': username, 'password': password})


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    cursor = conn.cursor()
    select_query = "SELECT id, name, email, level FROM members WHERE id = %s"
    cursor.execute(select_query, [member_id])
    one_member = cursor.fetchone()
    cursor.close()

    return jsonify(
        {'member': {'id': one_member[0], 'name': one_member[1], 'email': one_member[2], 'level': one_member[3]}})


@app.route('/member', methods=['POST'])
def add_member():
    new_member_data = request.get_json()

    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    cursor = conn.cursor()
    insert_query = "INSERT INTO members (name, email, level) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, [name, email, level])
    conn.commit()

    select_query = "SELECT id, name, email, level FROM members WHERE name = %s"
    cursor.execute(select_query, [name])
    new_member = cursor.fetchone()
    cursor.close()

    return jsonify({'id': new_member[0], 'name': new_member[1], 'email': new_member[2], 'level': new_member[3]})

    # return f'The name is {name}, the email is {email}, the level is {level}'


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    new_member_data = request.get_json()

    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    cursor = conn.cursor()
    select_query = "UPDATE members set name = %s, email = %s, level = %s WHERE id = %s"
    cursor.execute(select_query, [name, email, level, member_id])
    conn.commit()

    select_query = "SELECT id, name, email, level FROM members WHERE id = %s"
    cursor.execute(select_query, [member_id])
    one_member = cursor.fetchone()
    cursor.close()

    return jsonify(
        {'member': {'id': one_member[0], 'name': one_member[1], 'email': one_member[2], 'level': one_member[3]}})


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    cursor = conn.cursor()
    delete_query = "DELETE from members WHERE id = %s"
    cursor.execute(delete_query, [member_id])
    conn.commit()

    return jsonify({'messege': f'The member of ID {member_id} has been removed'})


if __name__ == '__main__':
    app.run(debug=True)
