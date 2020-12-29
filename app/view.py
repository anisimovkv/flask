from flask import render_template
from .app import app


@app.route('/')
def index():
    var = "Bla bla bla bla"
    return render_template('index.html', v=var)
