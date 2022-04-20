from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from flask_login import LoginManager
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'emyKFWDVMQwGjzv5dgfhHgot12nsrhiNZ'
manager = LoginManager()

aut = False
id = None
prof = None

menu = [{"name": "Главная", "url": "main"},
        {"name": "МЫ - ", "url": "about"},
        {"name": "ЧЕКАНУТЬ ПРОФИЛЬ", "url": "/profile/imichael"},
        {"name": "КАНТА АКТЫ", "url": "/contact"},
        {"name": "Войти", "url": "/login"},
        {"name": "Правила", "url": "/rules"},
        {"name": "Зарегистрироваться", "url": "/reg"}]


@app.route("/main")
def main():
    if aut:
        print(url_for('main'))
        return render_template('main.html', menu=menu)
    else:
        return redirect(url_for('login'))


@app.route("/about", methods=['POST', 'GET'])
def about():
    if aut:
        print(url_for('about'))
        if request.method == 'POST':
            return redirect(url_for('profile', username=session['userLogged']))

        return render_template('about.html', title="Хто я!", menu=menu)
    else:
        return redirect(url_for('login'))


'''@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"'''


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if aut:
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
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='404', menu=menu), 404


@app.errorhandler(401)
def pageNotYour(error):
    return render_template('page401.html', title='401', menu=menu), 401


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        if 'userLogged' in session:
            print('Hi')
            return redirect(url_for('main', username=session['userLogged']))
        else:
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
                print(el[1], el[2])
                if request.method == 'GET':
                    return redirect(url_for("main"), 304)

    return render_template('log.html', title='Авторизация')


@app.route("/rules")
def rules():
    return render_template('rules.html', title='Правила платформы', menu=menu)


'''
@app.route("/login", methods=["GET", "POST"])
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
            print(el[1], el[2])
            return redirect(url_for('main'))

    return render_template('log.html', title='Войти', menu=menu)'''


@app.route("/logout", methods=["GET", "POST"])
def logout():
    pass


@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == 'POST':
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
    return render_template('reg.html', title='Зарегистрироваться', menu=menu)


'''
with app.test_request_context():
    print( url_for('about') )'''

if __name__ == '__main__':
    app.run(debug=True)
