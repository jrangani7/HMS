from application import app
from flask import render_template,request,session ,flash,redirect,url_for
from application.forms import LoginForm
from application import mysql
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        
        n= mysql.connect().cursor().execute("SELECT * from userstore where loginid =%s and password=%s",(username,password))
        if n :
            session["username"] = username
            session.permanent = True
            if 'AD' in username:
                return render_template("desk/index.html",username=username,password=password)
            elif 'PH' in username:
                return render_template("pharmacy/index.html",username=username,password=password)
            return render_template("diagnostic/index.html",username=username,password=password)
        else:
            flash(' Invalid Credentials.')
            return redirect(url_for('login'))
    form=LoginForm()
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    session.pop("username",None)
    return redirecrt(url_for("login"))

@app.route('/home')
def home():
    if "username" in session:
        return render_template("home.html",username=session['username'])
    else:
        form=LoginForm()
        return render_template("login.html",form=form)
