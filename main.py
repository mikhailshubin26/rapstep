from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from flask_login import LoginManager
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'emyKFWDVMQwGjzv5dgfhHgot12nsrhiNZ'
manager = LoginManager()

menu = [{"name": "Главная", "url": "main"},
        {"name": "ЧЕКАНУТЬ ПРОФИЛЬ", "url": "/profile"},
        {"name": "КАНТА АКТЫ", "url": "/contact"},
        {"name": "Правила", "url": "/rules"},
        {"name": "Войти", "url": "/login"},
        {"name": "Зарегистрироваться", "url": "/reg"},
        {"name": "Выйти", "url": "/logout"}]


@app.route("/main")
def main():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        print(url_for('main'))
        return render_template('main.html', menu=menu)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            search = cur.execute("""SELECT * FROM persons""")
            for el in search:
                if el[1] == request.form['username']:
                    print("SHALOM")
                    return redirect("person")

        return render_template('profile.html', menu=menu)


@app.route("/person")
def man():
    return f"Пользователь: "


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if len(request.form['username']) > 2:
                flash('Сообщение отправлено', category='success')
                con = sqlite3.connect("users.sqlite")
                cur = con.cursor()
                us = request.form['username']
                em = request.form['email']
                ms = request.form['message']
                cur.execute(f'INSERT INTO asks (username, email, message) VALUES ("{us}", "{em}", "{ms}")')
                con.commit()
                cur.close()
            else:
                flash('Ошибка отправки. Слишком мало символов в имени', category='error')

        return render_template('contact.html', title='Обратная связь', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='404', menu=menu), 404


@app.errorhandler(401)
def pageNotYour(error):
    return render_template('page401.html', title='401', menu=menu), 401


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            res = cur.execute("""SELECT * FROM users""").fetchall()
            con.commit()
            cur.close()
            for el in res:
                if el[1] == request.form['username'] and request.form['psw'] == el[2]:
                    session['userLogged'] = request.form['username']
                    return redirect(url_for('main', username=session['userLogged']))
                flash('Неверный логин или пароль')

    # elif request.method == 'POST' and request.form['username'] == 'imichael' and request.form['psw'] == "123":
    #   session['userLogged'] = request.form['username']
    #  return redirect(url_for('index', username=session['userLogged']))

    return render_template('login.html', title='Авторизация')


@app.route("/rules")
def rules():
    return render_template('rules.html', title='Правила платформы', menu=menu)


'''@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == 'POST':
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users""").fetchall()
        con.commit()
        bl = False
        for el in result:
            if el[1] == request.form['username'] and el[2] == request.form["password"]:
                bl = True
        if bl:
            aut = True
            id = [0]
            prof = el[1]
            return redirect(url_for('main'))

    return render_template('log.html', title='Войти', menu=menu)'''


@app.route("/logout", methods=["GET", "POST"])
def logout():
    del session['userLogged']
    return redirect(url_for('login'))


@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == 'POST':
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM users""")
        flag = True
        for e in result:
            if e[1] == request.form['username']:
                flag = False
            else:
                continue
        if request.form['password'] == request.form['corpassword']:
            if flag:
                lg = request.form['username']
                ps = request.form['password']
                cur.execute(f'INSERT INTO users (login, password) VALUES ("{lg}", "{ps}")')
                cur.execute(f'INSERT INTO persons (own) VALUES ("{lg}")')
                con.commit()
                cur.close()
                return redirect(url_for('login'))

            else:
                flash('Логин уже занят')
        else:
            flash('Пароли не совпадают')
    return render_template('reg.html', title='Зарегистрироваться')


'''
with app.test_request_context():
    print( url_for('about') )'''

if __name__ == '__main__':
    app.run(debug=True)
