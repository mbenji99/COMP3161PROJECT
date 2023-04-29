from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('User ID', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    userID = StringField('User ID', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    account_type = SelectField('Account Type', choices=[('Lecturer', "Lecturer"), ("Student", 'Student')], validators=[InputRequired()])

class StudentRegistrationForm(FlaskForm):
    level = SelectField('Level of Study', choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('Doctorate', 'Doctorate')], validators=[InputRequired()])
    date_enrolled = DateField('Date Enrolled', validators=[InputRequired()])

class LecturerRegistrationForm(FlaskForm):
    salary = StringField('Salary', validators=[InputRequired()])

class CourseRegistration(FlaskForm):
    userID = StringField('User ID', validators=[InputRequired()])
    course_name = StringField('Course Name', validators=[InputRequired()])
    start_date = DateField('Course Start Date', validators=[InputRequired()])
    
