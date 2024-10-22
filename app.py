from flask import Flask, render_template, request
import sqlite3
import uuid

app = Flask(__name__)

# Function to create the database and table if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ambulances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ambulance_number TEXT UNIQUE,
            rfid_id TEXT,
            token TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    ambulance_number = request.form['ambulance_number']
    photo = request.files['photo']
    
    # Simulate RFID ID retrieval (for now, we'll use a static ID)
    rfid_id = "RFID-12345"  # Replace with actual RFID retrieval logic

    # Generate a unique token
    token = str(uuid.uuid4())

    # Store the ambulance information in the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO ambulances (ambulance_number, rfid_id, token) VALUES (?, ?, ?)',
                       (ambulance_number, rfid_id, token))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Ambulance number already exists.", 400
    finally:
        conn.close()

    # Redirect to success page with token
    return render_template('success.html', token=token, rfid_id=rfid_id)

if __name__ == '__main__':
    app.run(debug=True)

