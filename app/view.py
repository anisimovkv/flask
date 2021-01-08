from flask import render_template

from .app import app


@app.route('/')
def index():
    var = "Bla bla bla bla"
    return render_template('index.html', v=var)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
