# database.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  
            database='matrices_yorne',  
            user='root', 
            password=''  
        )
        if conn.is_connected():
            print("Conecta cool a la base de datos")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matrices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            matrix TEXT NOT NULL
        )
    ''')
    conn.commit()

def save_matrix(conn, matrix):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO matrices (matrix) VALUES (%s)', (matrix,))
    conn.commit()

def get_matrices(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM matrices')
    return cursor.fetchall()


conn = create_connection()
if conn:
    create_table(conn)
    conn.close()