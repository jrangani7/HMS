from application import app
from flask import render_template,request,session ,flash,redirect,url_for
from application.forms import LoginForm
from application import mysql
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    if 'username' in session:
        username=session['username']
        if 'AD' in username:
            return redirect(url_for('desk_home'))
        elif 'PH' in username:
            return render_template(url_for('pharmacy_home'))
        return render_template(url_for('diagnostic_home')) 
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        username=session['username']
        if 'AD' in username:
            return redirect(url_for('desk_home'))
        elif 'PH' in username:
            return render_template(url_for('pharmacy_home'))
        return render_template(url_for('diagnostic_home'))
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        
        n= mysql.connect().cursor().execute("SELECT * from userstore where loginid =%s and password=%s",(username,password))
        if n :
            session["username"] = username
            session.permanent = True
            if 'AD' in username:
                return redirect(url_for('desk_home'))
            elif 'PH' in username:
                return render_template(url_for('pharmacy_home'))
            return render_template(url_for('diagnostic_home'))
        else:
            flash(' Invalid Credentials.')
            return redirect(url_for('login'))
    form=LoginForm()
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop("username",None)
    return redirect(url_for("login"))

@app.route('/desk')
def desk_home():
    if 'username' in session and 'AD' in session['username']:
        return render_template("desk/index.html")
    return redirect(url_for('login'))

@app.route('/pharmacy')
def pharmacy_home():
    if 'username' in session and 'PH' in session['username']:
        return render_template("pharmacy/index.html")
    return redirect(url_for('login'))

@app.route('/diagnostic')
def diagnostic_home():
    if 'username' in session and 'DS' in session['username']:
        return render_template("diagnostic/index.html")
    return redirect(url_for('login'))

