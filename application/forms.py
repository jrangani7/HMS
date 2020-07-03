from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired,NumberRange
from wtforms.fields.html5 import DateField



#####################################################################################
class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])

#####################################################################################
# Patient Registration Form #
class PatientRegistrationForm(FlaskForm):
    pName=StringField('name',validators=[DataRequired()],)
    pAge=IntegerField('age',validators=[DataRequired(),NumberRange(message="Please fill appropriate age !",min=1,max=999)])
    dateOfSubmission=DateField('date',format='%Y-%m-%d')
    bedType=SelectField('bed',choices=[('General','General'),('Semi Sharing','Semi Sharing'),('Single','Single')])
    address=StringField('address',validators=[DataRequired()])
    city=StringField('city',validators=[DataRequired()])
    state=StringField('state',validators=[DataRequired()])
    uid=IntegerField('aadhar',validators=[DataRequired()])
    status=SelectField('status',choices=[('Active','Active'),('Discharged','Discharged')])
    
  ###################################################################################
### Patient Delete Form
class DeleteForm(FlaskForm):
    pid=IntegerField('patID',validators=[DataRequired()])

class SearchForm(FlaskForm):
    pid=IntegerField('patID',validators=[DataRequired()])

####################################################################################
class BillingForm(FlaskForm):
    pid=IntegerField('patID',validators=[DataRequired()])
#####################################################################################
# Patient Registration Form #
class UpdatePatientForm(FlaskForm):
    pid=IntegerField('patID',validators=[DataRequired()])
    pName=StringField('name',validators=[DataRequired()],)
    pAge=IntegerField('age',validators=[DataRequired(),NumberRange(message="Please fill appropriate age !",min=1,max=999)])
    dateOfSubmission=DateField('date',format='%Y-%m-%d')
    bedType=SelectField('bed',choices=[('General','General'),('Semi Sharing','Semi Sharing'),('Single','Single')])
    address=StringField('address',validators=[DataRequired()])
    city=StringField('city',validators=[DataRequired()])
    state=StringField('state',validators=[DataRequired()])
    uid=IntegerField('aadhar',validators=[DataRequired()])
    status=SelectField('status',choices=[('Active','Active'),('Discharged','Discharged')])

    def set_data(self,pdata):   
      """
      Function sets the patient object data to form
      """
      self.uid.data=pdata[0]
      self.pid.data=pdata[1]
      self.pName.data=pdata[2]
      self.pAge.data=pdata[3]
      self.dateOfSubmission.data=pdata[4]
      self.bedType.data=pdata[5]
      self.address.data=pdata[6]
      self.city.data=pdata[7]
      self.state.data=pdata[8]
      self.status.data=pdata[9]

#######################################################################################################
# patient search form
class SearchForm(FlaskForm):
    pid=IntegerField('patID',validators=[DataRequired()])

######################################################################################################
class IssueMedicineForm(FlaskForm):
    mid=IntegerField('med_id',validators=[DataRequired()])
    quantity=IntegerField('quantity',validators=[DataRequired()])
    dateOfIssue=DateField('doi',format='%Y-%m-%d',validators=[DataRequired()])


class IssueDiagnosticForm(FlaskForm):
    tid=IntegerField('test_id',validators=[DataRequired()])

