from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time
from psycopg2 import OperationalError

app = Flask(__name__)

# Database connection configuration
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'employeedb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def wait_for_postgres(host, user, password, db_name, max_attempts=10):
    attempt = 0
    while attempt < max_attempts:
        try:
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except OperationalError as e:
            print(f"Waiting for PostgreSQL... Attempt {attempt + 1}")
            print(f"Connection error: {e}")
            time.sleep(3)
            attempt += 1
    return False

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            position VARCHAR(100)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM employees')
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', employees=employees)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/add', methods=['POST'])
def add_employee():
    try:
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO employees (name, email, position) VALUES (%s, %s, %s)',
                    (name, email, position))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/delete/<int:id>')
def delete_employee(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM employees WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Wait for PostgreSQL to be ready
    if wait_for_postgres(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
        # Initialize the database
        init_db()
        
        # Start the Flask application
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Could not connect to PostgreSQL. Exiting.")
        exit(1)