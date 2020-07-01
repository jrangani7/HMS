from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,SelectField,IntegerField
from wtforms.validators import DataRequired,NumberRange


#####################################################################################
class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])

#####################################################################################
# Patient Registration Form #
class PatientRegistrationForm(FlaskForm):
    pName=StringField('name',validators=[DataRequired()])
    pAge=IntegerField('age',validators=[DataRequired(),NumberRange(min=1,max=999)])
    dateOfSubmission=DateField('date',format='%d-%m-%Y')
    bedType=SelectField('bed',validators=[DataRequired()],choices=['General','Semi Sharing','Single'])
    address=StringField('address')
    city=StringField('city')
    state=StringField('state')
    uid=IntegerField('aadhar')
    status=SelectField('status',validators=[DataRequired()],choices=['Active','Discharged'])
    
  ###################################################################################
### Patient Delete Form
class DeleteForm(FlaskForm):
    pid=IntegerField('patID')

class SearchForm(FlaskForm):
    pid=IntegerField('patID')

####################################################################################
class BillingForm(FlaskForm):
    pid=IntegerField('patID')
#####################################################################################
# Patient Registration Form #
class UpdatePatientForm(FlaskForm):
    pid=IntegerField('patID')
    pName=StringField('name',validators=[DataRequired()])
    pAge=IntegerField('age',validators=[DataRequired(),NumberRange(min=1,max=999)])
    dateOfSubmission=DateField('date',format='%d-%m-%Y')
    bedType=SelectField('bed',validators=[DataRequired()],choices=['General','Semi Sharing','Single'])
    address=StringField('address')
    city=StringField('city')
    state=StringField('state')
    uid=IntegerField('aadhar')
    status=SelectField('status',validators=[DataRequired()],choices=['Active','Discharged'])

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
    pid=IntegerField('patID')

