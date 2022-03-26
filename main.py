from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'emyKFWDVMQwGjzv5dgfhHgot12nsrhiNZ'

menu = [{"name": "Главная", "url" : "main"},
{"name": "МЫ - ", "url" : "about"},
{"name" : "ЧЕКАНУТЬ ПРОФИЛЬ", "url" : "/profile/leeroii"},
{"name" : "КАНТА АКТЫ", "url" : "/contact"}]

@app.route("/")
@app.route("/main")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="Хто я!", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"

@app.route("/contact", methods=["POST", "GET"])
def contact():

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


    return render_template('contact.html', title = 'Обратная связь', menu=menu)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='404', menu=menu), 404

@app.errorhandler(401)
def pageNotYour(error):
    return render_template('page401.html', title='401', menu=menu), 401

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'imichael' and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация')
'''
with app.test_request_context():
    print( url_for('about') )'''

if __name__ == '__main__':
    app.run(debug=True)
