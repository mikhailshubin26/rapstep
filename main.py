from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from flask_login import LoginManager
import sqlite3
import os
import bs4
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'emyKFWDVMQwGjzv5dgfhHgot12nsrhiNZ'
manager = LoginManager()

menu = [{"name": "Главная", "url": "main"},
        {"name": "Статьи", "url": "titles"},
        {"name": "Пользователи", "url": "profile"},
        {"name": "КАНТА АКТЫ", "url": "/contact"},
        {"name": "Правила", "url": "/rules"},
        {"name": "Войти", "url": "/logout"},
        {"name": "Зарегистрироваться", "url": "/reg"},
        {"name": "Выйти", "url": "/logout"}]

src = None
con = sqlite3.connect("users.sqlite")
cur = con.cursor()
sp = cur.execute("""SELECT * FROM home""").fetchall()
con.commit()
cur.close()
pages = []
for el in sp:
    el = list(el)
    pages.append([el[1], el[2], el[3][0:15], el[0]])

print(pages)
print(sp)
nsp = [{"name": f"{pages[-1][1]}", "url": f"{pages[-1][0]}"},
       {"name": f"{pages[-2][1]}", "url": f"{pages[-2][0]}"},
       {"name": f"{pages[-3][1]}", "url": f"{pages[-3][0]}"},
       {"name": f"{pages[-4][1]}", "url": f"{pages[-4][0]}"},
       {"name": f"{pages[-5][1]}", "url": f"{pages[-5][0]}"},
       {"name": f"{pages[-6][1]}", "url": f"{pages[-6][0]}"},
       {"name": f"{pages[-7][1]}", "url": f"{pages[-7][0]}"},
       {"name": f"{pages[-8][1]}", "url": f"{pages[-8][0]}"},
       {"name": f"{pages[-9][1]}", "url": f"{pages[-9][0]}"},
       {"name": f"{pages[-10][1]}", "url": f"{pages[-10][0]}"}, ]


@app.route("/main")
def main():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        print(url_for('main'))

        return render_template('main.html', menu=menu)

@app.route("/titles")
def titles():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        print(url_for('titles'))
        all = ''
        for i in range(0, 5):
            all += f'{sp[i][1]}         {pages[i][3]}\n'
            all += f'{sp[i][2]}\n'
            all += f'{sp[i][4]}\n'
            all += f'{sp[i][5]}\n\n\n\n\n'
        # all += f'{sp[5][1]}          {sp[5][2]}'
        # print(sp[5][1], sp[5][2], sp[5][3], sp[5][4], sp[5][5])
        # print(all)
        total = f"Статьи:\n{all}"
        return total



@app.route("/add", methods=['POST', 'GET'])
def add():
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        print(url_for('add'))
        print(request.method)
        if request.method == 'POST':
            print(len(request.form['message']))
            print(len(request.form['title']))
            print(len(request.form['contact']))
            if len(request.form['message']) > 15 or len(request.form['title']) > 5 or len(request.form['contact']) >= 0:
                flash('Опубликовано', category='success')
                con = sqlite3.connect("users.sqlite")
                cur = con.cursor()
                aut = session['userLogged']
                tt = request.form['title']
                ct = request.form['contact']
                ms = request.form['message']
                url = request.form['url']
                cur.execute(
                    f'INSERT INTO home (author, title, contact, message, url) VALUES ("{aut}" ,"{tt}", "{ct}", "{ms}", "{url}")')
                con.commit()
                cur.close()
            else:
                flash('Ошибка отправки. Слишком мало символов', category='error')

        return render_template('add.html', menu=menu)


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    global src
    if 'userLogged' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            search = cur.execute("""SELECT * FROM persons""")
            for el in search:
                if el[1] == request.form['username']:
                    src = request.form['username']
                    print("SHALOM")
                    return redirect("person")

        return render_template('profile.html', menu=menu)


@app.route("/person")
def man():
    return f"Пользователь: {src}"


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
