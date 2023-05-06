from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Load MySQL configurations from the config file
db_config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

@app.route('/init_db')
def init_db():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS employees (EmpID INTEGER PRIMARY KEY AUTO_INCREMENT, EmpName VARCHAR(255), EmpGender VARCHAR(255), EmpPhone VARCHAR(255), EmpBdate DATE)''')
    mysql.connection.commit()


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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (EmpName, EmpGender, EmpPhone, EmpBdate) VALUES (%s, %s, %s, %s)", (EmpName, EmpGender, EmpPhone, EmpBdate))
        mysql.connection.commit()
        return redirect(url_for('information'))
    return render_template('registration.html')

@app.route('/information')
def information():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    return render_template('information.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

