from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin')
def admin():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', result=result)


@app.route('/adminremove', methods=['GET', 'POST'])
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


@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('guestbook.html', result=result)


@app.route('/process', methods=['POST'])
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
    app.run(host='0.0.0.0', port=5000)
