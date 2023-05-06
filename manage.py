from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (EmpID INTEGER PRIMARY KEY AUTOINCREMENT, EmpName TEXT, EmpGender TEXT, EmpPhone TEXT, EmpBdate TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        EmpName = request.form['EmpName']
        EmpGender = request.form['EmpGender']
        EmpPhone = request.form['EmpPhone']
        EmpBdate = request.form['EmpBdate']

        conn = sqlite3.connect('employee.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees (EmpName, EmpGender, EmpPhone, EmpBdate) VALUES (?, ?, ?, ?)", (EmpName, EmpGender, EmpPhone, EmpBdate))
        conn.commit()
        conn.close()
        return redirect(url_for('information'))
    return render_template('registration.html')

@app.route('/information')
def information():
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    data = c.fetchall()
    conn.close()
    return render_template('information.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

