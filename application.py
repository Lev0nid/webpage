from flask import Flask, render_template, request, redirect
import sqlite3

application = Flask(__name__)


@application.route('/')
def home():
    return render_template('home.html')


@application.route('/admin')
def admin():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', result=result)


@application.route('/adminremove', methods=['GET', 'POST'])
def adminremove():
    name = request.form['name']
    comment = request.form['comment']
    password = request.form['password']
    if password != 'I<3Lenya':
        return '<h1>lmao wrong password</h1>'
    conn = sqlite3.connect('comments.db')
    conn.execute('DELETE FROM comments WHERE name=? AND comment=?;', (name, comment))
    conn.commit()
    conn.close()
    return redirect('/admin')


@application.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('guestbook.html', result=result)


@application.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    comment = request.form['comment']
    conn = sqlite3.connect('comments.db')
    if name != "" and comment != "":
        conn.execute('INSERT INTO comments (name, comment) VALUES (?, ?);', (name, comment))
        conn.commit()
    conn.close()
    return redirect('/guestbook')


if __name__ == '__main__':
    application.run(port=5000)
