from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)

# ----------------------
# Login API
# ----------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

# ----------------------
# CRUD APIs
# ----------------------
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, email, department, salary) VALUES (%s, %s, %s, %s)",
        (data['name'], data['email'], data['department'], data['salary'])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "Employee added"}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    conn.close()
    return jsonify(employee)

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET name=%s, email=%s, department=%s, salary=%s WHERE id=%s",
        (data['name'], data['email'], data['department'], data['salary'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "Employee updated"})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "Employee deleted"})

if __name__ == "__main__":
    app.run(debug=True)