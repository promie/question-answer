from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
# The secret key is necessary for the session to work
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']

        db = get_db()
        user_cur = db.execute('''
                    SELECT
                        id, name, password, expert, admin
                    FROM
                        users
                    WHERE
                        name = ?
        ''', [user])
        user_result = user_cur.fetchone()
    return user_result


@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', title='Home', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    user = get_current_user()
    if request.method == 'POST':
        db = get_db()
        name = request.form['name']
        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        db.execute('INSERT INTO users (name, password, expert, admin) VALUES (?,?,?,?)',\
                   [name, hashed_password, '0', '0'])
        db.commit()
        # Session created as soon as a new user is registered
        session['user'] = request.form['name']
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', user=user)


@app.route('/answer')
def answer():
    user = get_current_user()
    return render_template('answer.html', title='Answer',user=user)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    user = get_current_user()
    db = get_db()

    if request.method == 'POST':
        db.execute('INSERT INTO questions (question_text, asked_by_id, expert_id) VALUES (?, ?, ?)',\
                   [request.form['question'], user['id'], request.form['expert']])
        db.commit()
        return redirect(url_for('index'))

    expert_cur = db.execute('''
                SELECT
                    id, name, expert
                FROM
                    users
                WHERE
                    expert = 1
    ''')
    expert_results = expert_cur.fetchall()
    return render_template('ask.html', title='Ask',user=user, experts=expert_results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = get_current_user()
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
            return redirect(url_for('index'))
        else:
            return '<h1>The password that you have entered is incorrect</h1>'
    return render_template('login.html', title='Login', user=user)


@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html', title='Question', user=user)


@app.route('/unanswered')
def unanswered():
    user = get_current_user()
    db = get_db()
    unanswered_cur = db.execute('''
                    SELECT
                        q.question_text AS question_text, u.name AS name
                    FROM
                        questions q
                        JOIN users u ON u.id = q.asked_by_id
                    WHERE
                        q.answer_text IS NULL AND q.expert_id = ?
    ''', [user['id']])
    unanswered_results = unanswered_cur.fetchall()
    return render_template('unanswered.html', title="Unanswered", user=user, unanswered_questions=unanswered_results)


@app.route('/users')
def users():
    user = get_current_user()
    db = get_db()
    user_cur = db.execute('''
                SELECT
                    id, name, expert, admin
                FROM
                    users         
    ''')
    users_results = user_cur.fetchall()

    return render_template('users.html', title='Users', user=user, users_results=users_results)


@app.route('/promoted/<user_id>')
def promoted(user_id):
    db = get_db()
    db.execute('''
        UPDATE
            users
        SET
            expert = 1
        WHERE
            id = ?
    ''', [user_id])
    db.commit()
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
