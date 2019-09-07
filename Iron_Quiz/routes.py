from Iron_Quiz import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"