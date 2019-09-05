from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def renderName(name=1):
    return render_template('index.html', name=name)
    # return 'Hello'
