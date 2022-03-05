from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "12345"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Erw9jujw5er69rt!!"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE email=%s and password=%s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('error'))
    return render_template('login.html')

@app.route('/new', methods= ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if "one" in request.form and "two" in request.form and "three" in request.form and "four" in request.form:
            first_name = request.form['one']
            last_name = request.form['two']
            email = request.form['three']
            password = request.form['four']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            usernamecheck = cursor.execute("SELECT email FROM logininfo WHERE email=%s",(email, ))
            if usernamecheck != 0:
                return redirect(url_for('exist'))
            else:
                cursor.execute("INSERT INTO logininfo (first_name, last_name, email, password)VALUES(%s, %s, %s, %s)", (first_name, last_name, email, password))
                db.connection.commit()
                return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/new/profile', methods = ['GET', 'POST'])
def profile():
    if session['loginsuccess'] == True:
        return render_template('profile.html')

@app.route('/error', methods = ['GET','POST'])
def error():
    return render_template('error.html')

@app.route('/exist')
def exist():
    return render_template('exist.html')


if __name__ == '__main__':
    app.run(debug=True)

