from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField,FileField,HiddenField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('UserID', validators=[InputRequired()])
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
    courseCode = StringField('Course Code', validators=[InputRequired()])
    start_date = DateField('Course Start Date', validators=[InputRequired()])
    
class CreateCourse(FlaskForm):
    courseCode = StringField('Course Code', validators=[InputRequired()])
    course_name = StringField('Course Name', validators=[InputRequired()])
    start_date = DateField('Course Start Date', validators=[InputRequired()])
    credits = StringField('Credits', validators=[InputRequired()])
    
class Courses(FlaskForm):
    u_id = StringField('Lecturer/Student ID', validators=[InputRequired()])
    
class Sections(FlaskForm):
    section_name = StringField('Section Name', validators=[InputRequired()])

class Content(FlaskForm):
    section_id = StringField('Section ID', validators=[InputRequired()])
    details = StringField('Details', validators=[InputRequired()])
    file = FileField()


class Reports(FlaskForm):
    report_type = SelectField('Account Type', choices=[
        ("courses_50_or_more_students",'Courses with students >= 50'), 
        ('students_5_or_more_courses',"Students with Courses >= 5"),
        ('lecturers_3_or_more_courses',"Lecturers with Courses >= 3"),
        ('top_10_enrolled_courses',"Top 10 Enrolled Courses"),
        ('top_10_students_highest_averages',"Top 10 Students Highest Average"),
        ], validators=[InputRequired()])
    
class UploadForm(FlaskForm):
    file = FileField('Upload Course Content', validators=[InputRequired()])

class SubmitAssignment(FlaskForm):
    file = FileField('Upload Assignment', validators=[InputRequired()])

class CreateAssignment(FlaskForm):
    details = StringField("Assignment Name",validators=[InputRequired()])
    due_date = DateField('Assignment Due Date', validators=[InputRequired()])
    file = FileField('Upload Assignment', validators=[InputRequired()])
    
class getCalendarEvents(FlaskForm):
    date = DateField('Event Date', validators=[InputRequired()])
    stud_id = StringField("Student ID",validators=[InputRequired()])
    courseCode = StringField('Course Code', validators=[InputRequired()])
    name = StringField('Event Name', validators=[InputRequired()])
    details = StringField('Event details', validators=[InputRequired()])
    
    