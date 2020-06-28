from application import app
from flask import render_template,request,session
from application.forms import LoginForm


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        return render_template("home.html",username=username,password=password)

    form=LoginForm()
    return render_template("login.html",form=form)