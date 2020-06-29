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
    pAge=IntegerField('age',validators=[DataRequired(),NumberRange(min=1,max=100)])
    dateOfSubmission=DateField('date',format='%d-%m-%Y')
    bedType=SelectField('bed',validators=[DataRequired()],choices=['General','Semi Sharing','Single'])
    address=StringField('address')
    city=StringField('city')
    state=StringField('state')
    uid=IntegerField('aadhar')
    status=SelectField('status',validators=[DataRequired()],choices=['Active','Discharged'])
    

