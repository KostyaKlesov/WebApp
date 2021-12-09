import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = b'My_Key'
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()



@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    if not username or not password:
        flash('неправильный логин или пароль')
        return render_template('login.html')
    else:
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
        records = list(cursor.fetchall())
        if not records:
            flash('похоже, такого пользователя нет')
            return render_template('login.html')
        else:
            print(records)
            return render_template('account.html', full_name=records[0][1], username=records[0][2],password=records[0][3])


@app.route('/regi/', methods=['GET', 'POST'])
def regi():
    if request.method == 'GET':
        return render_template('regi.html')
    else:
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
        records = list(cursor.fetchall())
        if not records:
            cursor.execute(f"INSERT INTO service.users (full_name, login, password) VALUES ('{str(name)}','{str(username)}', '{str(password)}');")
            return redirect(url_for('login'))



if __name__=="__main__":
    app.run(port="5000")