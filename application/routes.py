from application import app
from flask import render_template,request,session ,flash,redirect,url_for
from application.forms import LoginForm, PatientRegistrationForm,SearchForm, DeleteForm,UpdatePatientForm,IssueMedicineForm,IssueDiagnosticForm, BillingForm
from application import mysql
from datetime import timedelta
from datetime import datetime
app.permanent_session_lifetime = timedelta(minutes=30)


######################################################################################
#Route to Login page 
@app.route('/',methods=['GET','POST'])
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
##Route to Logout page 
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
        return render_template("desk/index.html",desk_home_page=True)
    return redirect(url_for('login'))

#Routinhg for New Patient Registration page 
@app.route('/desk/patientRegistration',methods=['GET','POST'])
def desk_patient():
    if 'username' in session and 'AD' in session['username']:
        form=PatientRegistrationForm(request.form)
        if request.method=='POST':
            if form.validate():
                status=registerPatient(form)
                if status:
                    flash("Registration Sucessful !!")
                    return redirect(url_for("desk_patient")) # redirect clears the form when registration is succesfull
                else:
                    flash("Registration Not Successful ! Please check data and try again !")
                    return render_template("desk/patient_registration.html",form=form) #form is preserved to allow user to make changes
            else:
                err=list(form.errors.values())
                flash(str(err[0][0])) #first error is flashed in case of multiple errors
                return render_template("desk/patient_registration.html",form=form)
        else:
            return render_template("desk/patient_registration.html",form=form,desk_patient_registration_page=True)
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
#Routing for Delete Patient page  

@app.route('/desk/patientdelete',methods=['GET','POST'])

def desk_patientdel():
    if 'username' in session and 'AD' in session['username']:
        form=SearchForm(request.form)
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
                    return render_template("desk/patient_delete.html",rudtest=pdata,form=form,desk_patient_delete_page=True)
                else:
                    flash("Patient not Found")
                    return render_template("desk/patient_delete.html",rudtest=pdata,form=form,desk_patient_delete_page=True)
            elif request.form['action'] == 'delete':
                con=mysql.connect()
                cursor=con.cursor()
                query = "DELETE FROM patient WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                cursor.close()
                con.commit()
                con.close()
                return render_template("desk/patient_delete.html",form=form,desk_patient_delete_page=True)

        else:
            return render_template("desk/patient_delete.html",form=form,desk_patient_delete_page=True)
    else:
        return redirect(url_for('login'))


#################################################################################################
#Routing for Update Patient page  

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
                    return render_template("desk/patient_update.html",pid=form.pid.data,form=form,update=True,desk_patient_update_page=True)
                else:
                    flash("Patient not Found")
                    return render_template("desk/patient_update.html",form=form,update=False,desk_patient_update_page=True)
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
                return render_template("desk/patient_update.html",form=form,Update=False,desk_patient_update_page=True)
            else:
                #discard
                del session['pid']
                return render_template("desk/patient_update.html",form=form,update=False,desk_patient_update_page=True)
        else:
            
            return render_template("desk/patient_update.html",form=form,update=False,desk_patient_update_page=True)
    else:
        if 'username' in session:
            if 'PH' in session['username']:
                return redirect(url_for('pharmacy_home'))
            return redirect(url_for('diagnostic_home'))
        return redirect(url_for('login'))

#################################################################################################
#Routing for Search Patient page  

@app.route('/desk/patientsearch',methods=['GET','POST'])

def desk_patientsearch():
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
                    return render_template("desk/search.html",rudtest=pdata,form=form,desk_patient_search_page=True)
                else:
                    flash("Patient not Found")
                    return render_template("desk/search.html",rudtest=pdata,form=form,desk_patient_search_page=True)


        else:
            return render_template("desk/search.html",form=form,desk_patient_search_page=True)
    else:
        return redirect(url_for('login'))

################################################################################################
#Routing for Displaying Active Patients page 

@app.route('/desk/activepatients')
def activepatients():
    if 'username' in session and 'AD' in session['username']:
        curr = mysql.connect().cursor()
        curr.execute("select * from patient where status='Active'")
        data = curr.fetchall()
        if curr.rowcount > 0:
            return render_template("desk/activepatients.html",data=data,desk_patient_active_page=True)
        else:
            return render_template("desk/activepatients.html",desk_patient_active_page=True)

    else:
        if 'username' in session:
            if 'PH' in session['username']:
                return redirect(url_for('pharmacy_home'))
            return redirect(url_for('diagnostic_home'))
        else:
            return redirect(url_for('login'))


################################################################################################
#Routing for Patient Billing
@app.route('/desk/billing',methods=['GET','POST'])

def billpatient():
    if 'username' in session and 'AD' in session['username']:
        form=BillingForm(request.form)
        if request.method=='POST':
            if request.form['action'] == 'show':
                con=mysql.connect()
                cursor=con.cursor()
                query = "SELECT * FROM patient WHERE id = %s AND status='Active' "
                cursor.execute(query, (form.pid.data,))
                pdata=cursor.fetchall()
                q1 = "SELECT doadmission FROM patient WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                doa=cursor.fetchone()
                if doa:
                    doastr=str(doa[4])
                    bedtype= doa[5]
                    date_time_table = (datetime.strptime(doastr, '%Y-%m-%d'))
                    date_now_str = (datetime.today().strftime('%Y-%m-%d'))
                    date_now = (datetime.strptime(date_now_str, '%Y-%m-%d'))
                    delta = date_now - date_time_table
                    if(bedtype == 'Single'):
                        session['roomcharge']=(delta.days)*8000
                    elif(bedtype == 'Semi'):
                        session['roomcharge']=(delta.days)*4000
                    else:
                        session['roomcharge']=(delta.days)*2000
                    session['doa'] =abs(delta.days)
                    session['dod'] =date_now_str

                q2 = "SELECT medicine_inventory.mname,issued_medicines.quantity_issued,medicine_inventory.rate FROM medicine_inventory ,issued_medicines WHERE  medicine_inventory.mid =issued_medicines.mid AND issued_medicines.pid= %s "   
                cursor.execute(q2, (form.pid.data,))
                rdata=cursor.fetchall()
                i=0
                for row in rdata:
                    i=i+(row[1]*row[2])
                

                session['pharmtotal'] =i

                q3= "SELECT diagnostic_tests.tname,diagnostic_tests.charge FROM diagnostic_tests,diagnostic_tests_conducted WHERE diagnostic_tests.tid = diagnostic_tests_conducted.tid AND diagnostic_tests_conducted.pid= %s "
                cursor.execute(q3, (form.pid.data,))
                ddata=cursor.fetchall()
                i=0
                for row in ddata:
                    i=i+row[1]

                session['diagnostictotal'] =i

                cursor.close()
                con.commit()
                con.close()
                if pdata:
                    return render_template("desk/billing.html",rudtest=pdata,rdata=rdata,ddata=ddata,form=form,desk_patient_billing_page=True)
                else:
                    flash("Patient not Found")
                    return render_template("desk/billing.html",rudtest=pdata,rdata=rdata,ddata=ddata,form=form,desk_patient_billing_page=True)
            
            elif request.form['action'] == 'update':
                con=mysql.connect()
                cursor=con.cursor()
                query = "UPDATE patient SET status='Discharged' WHERE id = %s "
                cursor.execute(query, (form.pid.data,))
                cursor.close()
                con.commit()
                con.close()
                return render_template("desk/index.html")



        else:
            return render_template("desk/billing.html",form=form,desk_patient_billing_page=True)
    else:
        return redirect(url_for('login'))

#################################################################################################

''' Pharmacy Pages and Routes  '''

@app.route('/pharmacy')
def pharmacy_home():
    if 'username' in session and 'PH' in session['username']:
        return redirect(url_for("search_patients"))
    return redirect(url_for('login'))

@app.route('/pharmacy/search_medicines',methods=['GET','POST'])
def search_patients():
    if 'username' in session and 'PH' in session['username']:
            form = SearchForm(request.form)
            if request.method == 'POST':
                    con=mysql.connect()
                    
                    cursor1=con.cursor()
                    query1 = "SELECT * FROM patient WHERE id = %s "
                    cursor1.execute(query1, (form.pid.data))
                    pdata=cursor1.fetchall()


                    cursor2=con.cursor()
                    query2 = "select medicine_inventory.mname,issued_medicines.quantity_issued,medicine_inventory.rate,medicine_inventory.rate*issued_medicines.quantity_issued from medicine_inventory INNER JOIN issued_medicines ON medicine_inventory.mid = issued_medicines.mid where issued_medicines.pid = %s"
                    cursor2.execute(query2, (form.pid.data,))
                    mdata=cursor2.fetchall()

                    session['pdata']=pdata
                    session['mdata']=mdata
                    session['pid']=form.pid.data


                    cursor1.close()
                    cursor2.close()
                    con.commit()
                    con.close()
                
                    if pdata:
                        return redirect(url_for("display_patient_details"))
                    else:
                        flash("Patient is not registered! Please check ID again!")
                        return render_template("pharmacy/search_patient.html",form=form)
            
            else:
                return render_template("pharmacy/search_patient.html",form=form)
    else:
        return redirect(url_for('login'))


@app.route('/pharmacy/display_details',methods=['GET','POST'])
def display_patient_details():
    if 'username' in session and 'PH' in session['username']:
       return render_template('pharmacy/display_patient_details.html',pdata=session['pdata'],mdata=session['mdata'])
    else:
        return redirect(url_for('login'))



@app.route('/pharmacy/issue_medicines',methods=['GET','POST'])
def issue_medicines():
    meddata=get_med_inventory()
    if 'username' in session and 'PH' in session['username']:
        form=IssueMedicineForm(request.form)
        if request.method=="POST":
            issueid=form.mid.data
            quantity=form.quantity.data
            doi=form.dateOfIssue.data
            if meddata:
                med=get_medicine(issueid)
                if issueid==med[0][0]:
                    if quantity<=med[0][2]:
                        status=issue(issueid,quantity,doi)
                        meddata=update_inventory(quantity,issueid)
                        if status:
                            flash("Medicines Issued and Database Updated !")
                            return redirect(url_for('issue_medicines')) #clear form previous input if succesfull
                        else:
                            flash("Something Went Wrong !")
                            return render_template('pharmacy/issue_medicines.html',form=form,meddata=meddata)
                    else:
                        flash("Medicine not available in that quantity !")
                        return render_template('pharmacy/issue_medicines.html',form=form,meddata=meddata)
                else:
                    flash("Medicine not in Database !")
                    return render_template('pharmacy/issue_medicines.html',form=form,meddata=meddata)
            else:
                flash("Out of Medicines !")
                return render_template('pharmacy/issue_medicines.html',form=form,meddata=meddata)
        else:
            return render_template('pharmacy/issue_medicines.html',form=form,meddata=meddata)
    else:
        return redirect(url_for('login'))

#Get Medicine to be issued
def get_medicine(issueid):
    con=mysql.connect()
    cursor=con.cursor()
    cursor.execute("SELECT * FROM medicine_inventory WHERE mid=%s",issueid)
    med=cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    return med

#Get Complete updated Medicine Inventory
def get_med_inventory():
        con=mysql.connect()
        cursor=con.cursor()
        cursor.execute("SELECT * FROM medicine_inventory ")
        meddata=cursor.fetchall()
        cursor.close()
        con.commit()
        con.close()
        return meddata

#Issue the required medicine
def issue(issueid,quantity,doi):
    try:
        con=mysql.connect()
        cursor=con.cursor()
        cursor.execute("INSERT INTO issued_medicines VALUES(%s,%s,%s)",(session['pid'],issueid,quantity))
        con.commit()
        cursor.close()
        con.close()
        return True
    except:
        return False 

#Update Inventory after issuing
def update_inventory(quantity,issueid):
    con=mysql.connect()
    con=mysql.connect()
    cursor=con.cursor()
    cursor.execute("UPDATE medicine_inventory SET quantity = quantity-%s WHERE mid = %s and quantity >= 0",(quantity,issueid))
    cursor1=con.cursor()
    cursor1.execute("SELECT * FROM medicine_inventory")
    meddata=cursor1.fetchall()
    con.commit()
    cursor1.close()
    cursor.close()
    con.close()
    return meddata
       


#################################################################################################

'''Diagnostics Pages and Routes '''

@app.route('/diagnostic')
def diagnostic_home():
    if 'username' in session and 'DS' in session['username']:
        return render_template("diagnostic/index.html")
    return redirect(url_for('login'))



@app.route('/diagnostic/search_diagnostics',methods=['GET','POST'])
def search_diagnostics():
    if 'username' in session and 'DS' in session['username']:
            form = SearchForm(request.form)
            if request.method == 'POST':
                    con=mysql.connect()
                    
                    cursor1=con.cursor()
                    query1 = "SELECT * FROM patient WHERE id = %s "
                    cursor1.execute(query1, (form.pid.data))
                    pdata=cursor1.fetchall()


                    cursor2=con.cursor()
                    query2 = "select diagnostic_tests.tid,diagnostic_tests.tname,diagnostic_tests.charge FROM diagnostic_tests INNER JOIN diagnostic_tests_conducted ON diagnostic_tests.tid = diagnostic_tests_conducted.tid where diagnostic_tests_conducted.pid = %s"
                    cursor2.execute(query2, (form.pid.data))
                    ddata=cursor2.fetchall()

                    session['pdata']=pdata
                    session['ddata']=ddata
                    session['pid']=form.pid.data


                    cursor1.close()
                    cursor2.close()
                    con.commit()
                    con.close()
                
                    if pdata:
                        return redirect(url_for("display_diagnostic_details"))
                    else:
                        flash("Patient is not registered! Please check ID again!")
                        return render_template("diagnostic/search_diagnostics.html",form=form)
            
            else:
                return render_template("diagnostic/search_diagnostics.html",form=form)
    else:
        return redirect(url_for('login'))




@app.route('/diagnostic/display_details',methods=['GET','POST'])
def display_diagnostic_details():
    if 'username' in session and 'DS' in session['username']:
       return render_template('diagnostic/display_diagnostic_details.html',pdata=session['pdata'],ddata=session['ddata'])
    else:
        return redirect(url_for('login'))


@app.route('/diagnostic/issue_diagnostics',methods=['GET','POST'])
def issue_diagnostics():
    testdata=available_tests()
    if 'username' in session and 'DS' in session['username']:
        form=IssueDiagnosticForm(request.form)
        if request.method=="POST":
            issueid=form.tid.data
            test=get_diagnostic(issueid)
            if test:
                if issueid==test[0][0]:
                    status=issue_test(issueid)
                    if status:
                        flash("Diagnosic Tests Issued!")
                        return render_template('diagnostic/issue_diagnostics.html',form=form,diagdata=testdata)
                    else:
                        flash("Something Went Wrong !")
                        return render_template('diagnostic/issue_diagnostics.html',form=form,diagdata=testdata)
                    
                else:
                    flash("Test not available !")
                    return render_template('diagnostic/issue_diagnostics.html',form=form,diagdata=testdata)
            else:
                flash("Wrong Test Id ! Please refer Available Tests 1")
                return render_template('diagnostic/issue_diagnostics.html',form=form,diagdata=testdata)
        else:
            return render_template('diagnostic/issue_diagnostics.html',form=form,diagdata=testdata)
    else:
        return redirect(url_for('login'))

#get required diagnostic
def get_diagnostic(issueid):
    con=mysql.connect()
    cursor=con.cursor()
    cursor.execute("SELECT * FROM diagnostic_tests WHERE tid=%s",issueid)
    med=cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()
    return med

#issue the test
def issue_test(issueid):
    try:
        con=mysql.connect()
        cursor=con.cursor()
        cursor.execute("INSERT INTO diagnostic_tests_conducted VALUES(%s,%s)",(session['pid'],issueid))
        con.commit()
        cursor.close()
        con.close()
        return True
    except:
        return False 

#get available tests for reference
def available_tests():
        con=mysql.connect()
        cursor=con.cursor()
        cursor.execute("SELECT * FROM diagnostic_tests ")
        data=cursor.fetchall()
        cursor.close()
        con.commit()
        con.close()
        return data
    
##################################################################################################
