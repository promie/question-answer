from flask import Flask

app = Flask(__name__)

# Up To Install and Templates

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
