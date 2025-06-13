from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__, static_folder='static')

# Initialize DB
def init_db():
    conn = sqlite3.connect('resume.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        experience INTEGER,
        resume TEXT
    )''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# Home route for form
@app.route('/')
def home():
    return render_template('demo.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    skills = request.form['skills']
    experience = request.form['experience']
    resume = request.form['resume']

    conn = sqlite3.connect('resume.db')
    c = conn.cursor()

    # Check if email already exists
    c.execute("SELECT * FROM candidates WHERE email = ?", (email,))
    existing = c.fetchone()

    if existing:
        conn.close()
        return render_template('already_submitted.html', email=email)

    # Insert new candidate
    c.execute("INSERT INTO candidates (name, email, phone, skills, experience, resume) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, phone, skills, experience, resume))
    conn.commit()
    conn.close()

    return render_template('thankyou.html', name=name)

# Admin page route
@app.route('/admin')
def admin():
    conn = sqlite3.connect('resume.db')
    c = conn.cursor()
    c.execute("SELECT * FROM candidates")
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
