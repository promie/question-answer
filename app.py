from flask import Flask, render_template, g, request, session
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
# The secret key is necessary for the session to work
app.config['SECRET_KEY'] = os.urandom(24)


# Session
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    user = None
    if 'user' in session:
        user = session['user']
    return render_template('home.html', title='Home', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        name = request.form['name']
        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        db.execute('INSERT INTO users (name, password, expert, admin) VALUES (?,?,?,?)',\
                   [name, hashed_password, '0', '0'])
        db.commit()

        return f'<h1>New User Created</h1>'
    return render_template('register.html', title='Register')


@app.route('/answer')
def answer():
    return render_template('answer.html', title='Answer')


@app.route('/ask')
def ask():
    return render_template('ask.html', title='Ask')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        name = request.form['name']
        password = request.form['password']

        user_cur = db.execute('''
                    SELECT
                        id, name, password
                    FROM
                        users
                    WHERE
                        name = ?
        ''', [name])
        user_result = user_cur.fetchone()

        if check_password_hash(user_result['password'], password):
            session['user'] = user_result['name']
        else:
            return '<h1>The password that you have entered is incorrect</h1>'
    return render_template('login.html', title='Login')


@app.route('/question')
def question():
    return render_template('question.html', title='Question')


@app.route('/unanswered')
def unanswered():
    return render_template('unanswered.html', title="Unanswered")


@app.route('/users')
def users():
    return render_template('users.html', title='Users')


if __name__ == '__main__':
    app.run(debug=True)
