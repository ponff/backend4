from flask import Flask, request, jsonify, render_template
import sqlite3
from threading import Lock

app = Flask(__name__)
db_path = 'aplications.db'
db_lock = Lock()

def get_db_connection():
    conn = None
    with db_lock:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    return conn, cursor

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_application():
    conn, cursor = get_db_connection()
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    attachment = request.files.getlist('attachment')[0]
        
    cursor.execute("""INSERT INTO applications (name, email, message, attachment_file) VALUES (?,?,?,?);""",
    (name, email, message, attachment.filename))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status':'success'}), 200
    


if __name__ == '__main__':
  con, cursor = get_db_connection()
  create_table_query = """
  CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    attachment_file TEXT
  );
  """
  cursor.execute(create_table_query)
  con.commit()
  cursor.close()
  con.close()
  app.run(debug=True host="0.0.0.0", port=81)
