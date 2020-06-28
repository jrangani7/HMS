from application import app
from flask import render_template,request,session


@app.route('/')
def index():
    return render_template("index.html")

