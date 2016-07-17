from flask import render_template
from peacemaker import app


@app.route('/')
def make_peace():
    return render_template('basic.html')

app.static_folder = 'static'
