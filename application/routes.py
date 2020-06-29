from application import app
from flask import render_template,request,session ,flash,redirect,url_for
from application.forms import LoginForm, PatientRegistrationForm, DeleteForm
from application import mysql
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=30)

######################################################################################

@app.route('/')
def index():
    if 'username' in session:
        username=session['username']
        if 'AD' in username:
            return redirect(url_for('desk_home'))
        elif 'PH' in username:
            return redirect(url_for('pharmacy_home'))
        return redirect(url_for('diagnostic_home')) 
    return render_template("index.html")

######################################################################################
@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        username=session['username']
        if 'AD' in username:
            return redirect(url_for('desk_home'))
        elif 'PH' in username:
            return redirect(url_for('pharmacy_home'))
        return redirect(url_for('diagnostic_home'))
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
                return redirect(url_for('pharmacy_home'))
            return redirect(url_for('diagnostic_home'))
        else:
            flash(' Invalid Credentials.')
            return redirect(url_for('login'))
    form=LoginForm()
    return render_template("login.html",form=form)

#################################################################################################
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop("username",None)
    return redirect(url_for("login"))

#################################################################################################
#Route app to desk if user is a Desk Administrator 
@app.route('/desk')
def desk_home():
    if 'username' in session and 'AD' in session['username']:
        return render_template("desk/index.html")
    return redirect(url_for('login'))

@app.route('/desk/patientRegistration',methods=['GET','POST'])
def desk_patient():
    if 'username' in session and 'AD' in session['username']:
        form=PatientRegistrationForm(request.form)
        if request.method=='POST':
            status=registerPatient(session['username'],form)
            if status:
                flash("Registration Sucessfull !!")
                return redirect(url_for("desk_patient")) # redirect clears the form when registration is succesfull
            else:
                flash("Registration Not Successfull ! Please check data and try again !")
                return render_template("desk/patient_registration.html",form=form) #form is preserved to allow user to make changes
        else:
            return render_template("desk/patient_registration.html",form=form)
    else:
        return redirect(url_for('login'))

def registerPatient(uid,form):
    try:
        con=mysql.connect()
        cursor=con.cursor()
        status=cursor.execute("INSERT INTO patient(uid,name,age,doadmission,bedtype,address,city,state,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uid,form.pName.data,form.pAge.data,form.dateOfSubmission.data,form.bedType.data,form.address.data,form.city.data,form.state.data,form.status.data))
        con.commit()
        con.close()  
        return status 
    except:
        return False #We can add more elaborate exceptions but it doesn't seem like a priority.

     


#################################################################################################
@app.route('/desk/patientdelete',methods=['GET','POST'])

def desk_patientdel():
    if 'username' in session and 'AD' in session['username']:
        form=DeleteForm(request.form)
        if request.method=='POST':
            if request.form['action'] == 'show':
                con=mysql.connect()
                cursor=con.cursor()
                query = "SELECT * FROM patient WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                ##cursor.execute("SELECT * FROM patient WHERE id = %s ",(form.pid.data))
                pdata=cursor.fetchall()
                cursor.close()
                con.commit()
                con.close()
                if pdata:
                    return render_template("desk/patient_delete.html",rudtest=pdata,form=form)
                else:
                    flash("Patient not Found")
                    return render_template("desk/patient_delete.html",rudtest=pdata,form=form)
            elif request.form['action'] == 'delete':
                con=mysql.connect()
                cursor=con.cursor()
                query = "DELETE FROM patient WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                ##cursor.execute("SELECT * FROM patient WHERE id = %s ",(form.pid.data))
                cursor.close()
                con.commit()
                con.close()
                return render_template("desk/patient_delete.html",form=form)

        else:
            return render_template("desk/patient_delete.html",form=form)
    else:
        return redirect(url_for('login'))


#################################################################################################
@app.route('/pharmacy')
def pharmacy_home():
    if 'username' in session and 'PH' in session['username']:
        return render_template("pharmacy/index.html")
    return redirect(url_for('login'))

#################################################################################################
@app.route('/diagnostic')
def diagnostic_home():
    if 'username' in session and 'DS' in session['username']:
        return render_template("diagnostic/index.html")
    return redirect(url_for('login'))

################################################################################################