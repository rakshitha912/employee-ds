import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="your_password",
        database="employee_db"
    )
    return conn
