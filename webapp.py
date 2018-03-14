from flask import (Flask, render_template, request, session,
                   redirect, url_for, Markup, flash)

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.secret_key = 'itsmybirthdaythatsthepassword'
    app.run(debug=True)
