from flask import Flask, render_template, g, request
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Login
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('home.html', title='Home')


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


@app.route('/login')
def login():
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
