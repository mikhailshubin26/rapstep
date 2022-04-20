import sqlite3

con = sqlite3.connect("users.sqlite")
cur = con.cursor()
result = cur.execute("""SELECT * FROM users""").fetchall()
con.commit()
con.close()
for el in result:
    print(f'Логин - {el[1]}')
    print(f'Пароль - {el[2]}')
    print('----------------------------------------')