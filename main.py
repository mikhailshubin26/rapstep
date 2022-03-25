from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)



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
    return f"Пользователь: {username}"

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        us = request.form['username']
        em = request.form['email']
        ms = request.form['message']
        cur.execute(f'INSERT INTO asks (username, email, message) VALUES ("{us}", "{em}", "{ms}")')
        con.commit()
        cur.close()

    return render_template('contact.html', title = 'Обратная связь', menu=menu)

'''
with app.test_request_context():
    print( url_for('about') )'''

if __name__ == '__main__':
    app.run(debug=True)
