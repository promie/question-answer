from flask import Flask, render_template
from database import get_db

app = Flask(__name__)


# Up To Install and Templates
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('home.html', title='Home')


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


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/unanswered')
def unanswered():
    return render_template('unanswered.html', title="Unanswered")


@app.route('/users')
def users():
    return render_template('users.html', title='Users')


if __name__ == '__main__':
    app.run(debug=True)
