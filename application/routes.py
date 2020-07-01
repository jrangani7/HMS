from application import app
from flask import render_template,request,session ,flash,redirect,url_for
from application.forms import LoginForm, PatientRegistrationForm,SearchForm, IssueMedForm, DeleteForm,UpdatePatientForm
from application import mysql
from datetime import timedelta
from datetime import datetime

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
            status=registerPatient(form)
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

def registerPatient(form):
    try:
        con=mysql.connect()
        cursor=con.cursor()
        status=cursor.execute("INSERT INTO patient(uid,name,age,doadmission,bedtype,address,city,state,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(form.uid.data,form.pName.data,form.pAge.data,form.dateOfSubmission.data,form.bedType.data,form.address.data,form.city.data,form.state.data,form.status.data))
        con.commit()
        con.close()  
        return status 
    except:
        return False #We can add more elaborate exceptions but it doesn't seem like a priority.

#################################################################################################
#Delete Patient  

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
                cursor.close()
                con.commit()
                con.close()
                return render_template("desk/patient_delete.html",form=form)

        else:
            return render_template("desk/patient_delete.html",form=form)
    else:
        return redirect(url_for('login'))


#################################################################################################
#Update Patient  

@app.route('/desk/patient_update',methods=['GET','POST'])

def desk_patient_update():
    if 'username' in session and 'AD' in session['username']:
        form=UpdatePatientForm(request.form)
        if request.method=='POST':
            if request.form['action'] == 'show':
                
                con=mysql.connect()
                cursor=con.cursor()
                query = "SELECT * FROM patient WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                pdata=cursor.fetchall()
                cursor.close()
                con.commit()
                con.close()
                
                
                if pdata:
                    form.set_data(pdata[0])
                    session["pid"]=form.pid.data
                    return render_template("desk/patient_update.html",pid=form.pid.data,form=form,update=True)
                else:
                    flash("Patient not Found")
                    return render_template("desk/patient_update.html",form=form,update=False)
            elif request.form['action'] == 'update':
                con=mysql.connect()
                cursor=con.cursor()

                query = "UPDATE patient SET uid = %s,name = %s,age = %s,doadmission = %s,bedtype = %s,address = %s,city = %s,state = %s,status = %s WHERE id = %s"
                data = (form.uid.data,form.pName.data,form.pAge.data,form.dateOfSubmission.data,form.bedType.data,
                        form.address.data,form.city.data,form.state.data,form.status.data,session['pid'])
                cursor.execute(query, data)
                cursor.close()
                con.commit()
                con.close()
                del session['pid']
                flash('Patient Details Updated.')
                return render_template("desk/patient_update.html",form=form,Update=False)
            else:
                #discard
                del session['pid']
                return render_template("desk/patient_update.html",form=form,update=False)
        else:
            
            return render_template("desk/patient_update.html",form=form,update=False)
    else:
        if 'username' in session:
            if 'PH' in session['username']:
                return redirect(url_for('pharmacy_home'))
            return redirect(url_for('diagnostic_home'))
        return redirect(url_for('login'))


################################################################################################
@app.route('/desk/activepatients')
def activepatients():
    if 'username' in session and 'AD' in session['username']:
        curr = mysql.connect().cursor()
        curr.execute("select * from patient where status='Active'")
        data = curr.fetchall()
        if curr.rowcount > 0:
            return render_template("desk/activepatients.html",data=data)
        else:
            return render_template("desk/activepatients.html")

    else:
        if 'username' in session:
            if 'PH' in session['username']:
                return redirect(url_for('pharmacy_home'))
            return redirect(url_for('diagnostic_home'))
        else:
            return redirect(url_for('login'))


#################################################################################################
@app.route('/pharmacy')
def pharmacy_home():
    if 'username' in session and 'PH' in session['username']:
        return render_template("pharmacy/index.html")
    return redirect(url_for('login'))

@app.route('/pharmacy/issue_medicines',methods=['GET','POST'])
def pharmacy_issue_medicines():
    if 'username' in session and 'PH' in session['username']:
            form = SearchForm(request.form)
            if request.method == 'POST':
                if request.form['action'] == 'show':
                    con=mysql.connect()
                    
                    cursor1=con.cursor()
                    query1 = "SELECT * FROM patient WHERE id = %s "
                    cursor1.execute(query1, (form.pid.data,))
                    pdata=cursor1.fetchall()

                    cursor2=con.cursor()
                    query2 = "select medicine_inventory.mname,issued_medicines.quantity_issued,medicine_inventory.rate,medicine_inventory.rate*issued_medicines.quantity_issued,issued_medicines.doi from medicine_inventory INNER JOIN issued_medicines ON medicine_inventory.mid = issued_medicines.mid where issued_medicines.pid = %s"
                    cursor2.execute(query2, (form.pid.data,))
                    mdata=cursor2.fetchall()

                    cursor1.close()
                    cursor2.close()
                    con.commit()
                    con.close()
                
                    if pdata:
                        return render_template("pharmacy/display_patient_medicines.html",pdata=pdata,mdata=mdata,form=form,update=1)
                    else:
                        flash("Patient not Found")
                        return render_template("pharmacy/display_patient_medicines.html",form=form)
             
                elif request.form['action'] == 'issue':
                    session["issue_med"] = form.pid.data
                    return redirect(url_for("pharmacy_issue_medicines_s2"))
                    
            else:
                return render_template("pharmacy/display_patient_medicines.html",form=form)
    
    else:
        return redirect(url_for('login'))
#################################################################################################
# Issue medicine Screen 2
@app.route('/pharmacy/issuemeds2',methods=['GET','POST'])
def pharmacy_issue_medicines_s2():
    if 'username' in session and 'PH' in session['username']:
        form = IssueMedForm(request.form)
        if request.method == 'POST': 
            
            if session['issue_med']:
                
                if request.form['action'] == 'check':
                    con=mysql.connect()
                        
                    cursor1=con.cursor()
                    query1 = "SELECT * FROM medicine_inventory WHERE mname = %s"
                    cursor1.execute(query1, (form.mname.data,))
                    mdata=cursor1.fetchall()
                    cursor1.close()
                    con.commit()
                    con.close()

                    if mdata:
                        if mdata[0][2] >= form.quantity.data:
                            flash("Medicine Available")
                            session['mid'] = mdata[0][0]
                            return render_template("pharmacy/issuemeds2.html",mdata=mdata,form=form)
                        else:
                            flash("Insufficient quantity in the inventory. "+str(mdata[0][2])+" available.")
                            return render_template("pharmacy/issuemeds2.html",form=form)
                    else:
                        flash("Medicine unavailable")
                        return render_template("pharmacy/issuemeds2.html",form=form)
                else:
                    con=mysql.connect()
                    cursor1=con.cursor()
                    cursor2=con.cursor()
                    query1 = "UPDATE medicine_inventory set quantity = quantity -"+str(form.quantity.data)+" WHERE mname = %s and quantity >= 0"
                    qry2 = "insert into issued_medicines values(%s,%s,%s,%s)"
                    cursor1.execute(query1, (form.mname.data,))
                    cursor2.execute(qry2, (session['issue_med'],session['mid'],form.quantity.data,datetime.today().strftime('%Y-%m-%d')))
                    cursor1.close()
                    cursor2.close()
                    con.commit()
                    con.close()
                    del session['mid']
                
                    flash("Medicine Issued")
                    return render_template("pharmacy/issuemeds2.html",form=form)
            else:
                return redirect(url_for("pharmacy_issue_medicines"))
        else:
            return render_template("pharmacy/issuemeds2.html",form=form)
    else:
        del session['isseu_med']
        return redirect(url_for('login'))


#################################################################################################
@app.route('/pharmacy/medicine_inventory')
def medicine_inventory():
    if 'username' in session and 'PH' in session['username']:
        curr = mysql.connect().cursor()
        curr.execute("select * from medicine_inventory")
        data = curr.fetchall() 
        return render_template("pharmacy/medicine_inventory.html",data=data)
    return redirect(url_for('login'))


#################################################################################################
@app.route('/diagnostic')
def diagnostic_home():
    if 'username' in session and 'DS' in session['username']:
        return render_template("diagnostic/index.html")
    return redirect(url_for('login'))


'''
query : select medicine_inventory.mname,issued_medicines.quantity_issued,medicine_inventory.rate,medicine_inventory.rate*issued_medicines.quantity_issued from medicine_inventory INNER JOIN issued_medicines ON medicine_inventory.mid = issued_medicines.mid where issued_medicines.pid = 2

'''