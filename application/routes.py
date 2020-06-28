from application import app
from flask import render_template,request,session
from .forms import LoginForm


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    form=LoginForm()
    return render_template("login.html",form=form)

@app.route('/home')
def home():
    return render_template("home.html")

