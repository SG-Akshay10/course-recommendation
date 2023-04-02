import flask
import pymysql
from flask import Flask, request, redirect, url_for, render_template, session

app = Flask(__name__)

# MySQL configurations
app.secret_key = "3yLj3t5EYr%9#ZyP7cGc0"
conn = pymysql.connect(host="localhost", user="root", password="sriheera", database="mlcia2")
cursor = conn.cursor()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['id'] = data[0]
            session['username'] = data[1]
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_id = session.get('id')
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_id))
        data = cursor.fetchone()
        if data:
            if new_password == confirm_password:
                cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
                conn.commit()
                return redirect(url_for('home'))
            else:
                return "New password and confirm password does not match."
        else:
            return "Incorrect current password."
    return render_template('forgot.html')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
