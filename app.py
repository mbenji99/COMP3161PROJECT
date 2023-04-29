from flask import Flask,make_response,request,session,render_template
from flask_login import current_user,LoginManager
import DBManager as dbm
import forms

app = Flask(__name__)
app.secret_key = 'something'

login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session['userID']

@app.route('/')
def index():
    return make_response({"Course":"COMP3161 - Intro to Database Management Systems"},200)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
        form = forms.RegistrationForm()
        return render_template('registration.html',form=form)
    
    userID = request.form.get('User ID')
    passW = request.form.get('Password')
    fName= request.form.get('First Name')
    lName= request.form.get('Last Name')
    userType = request.form.get('Account Type')
    email = request.form.get('Email')
    
    if userID is None or passW is None or fName is None or lName is None or userType is None or email is None:
        return make_response("Please ensure there is something in all fields before submitting",404)
    
    if userID[:3] == "620" and len(userID) <= 9:
        dbm.register_user({"userID":userID,"passW":passW,"userType":userType,"fName":fName,"lName":lName})
        return make_response({"Status":"Success"},200)
    else:
        return make_response({"Status": "Invalid user id."},404)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "GET":
        form = forms.LoginForm()
        return render_template('login.html',form=form)
    
    userID = request.form.get('User ID')
    passW = request.form.get('Password')
    
    if userID is None or passW is None:
        return make_response("Please enter something in all fields to login",404)
    
    res = dbm.login_user(userID,passW)
    
    if res is None:
        return make_response("Error. Plese ensure login credentials are correct and try again.",404)
    
    session['userType'] = res
    session['userID'] = userID
    return make_response("Successful login",200)

@app.route('/logout')
def logout():
    if not session.get('userType'):
        return make_response("Go to /login to login.",404)
    session.pop('userType')  
    session.pop('userID')

@app.route('/create_course', methods=['POST'])
def createCourse():
    if not session.get('userType'):
        return make_response("Login to create courses",404)
    
    if session['userType'] != "ADMIN":
        return make_response("Only admins can access this page and you are not one.", 404)
    
    courseCode = request.form.get("course_code")
    course_name = request.form.get('course_name')
    start_date = request.form.get('start_date')
    credits = request.form.get('credits')
    
    if courseCode is None or course_name is None or start_date is None or credits is None:
        return make_response("Please ensure there is something in all fields before submitting",404)

    dbm.create_course({"courseCode": courseCode, "course_name": course_name, "start_date": start_date, "credits": credits})

    return make_response({"Status": "Course created successfully.", "courseCode": courseCode}, 200)
   
@app.route('/courses',methods=['GET','POST'])
def get_courses():
    if not session.get('userType'):
        return make_response("Login to view courses",404)
    
    if request.method == "GET":
        courses = dbm.get_courses("All")
        return make_response(courses,200)

    u_id = request.form.get('u_id')
    courses = dbm.get_courses_by_id(u_id)
    
    if courses is not None:
        return make_response(courses,200)
    
    return make_response("That id does not exist or is not registered for any course",404)
        
   
@app.route('/register_course', methods=['GET','POST'])
def register_course():
    if not session.get('userType'):
        return make_response("Login to register for courses",404)
    
    if request.method == "GET":
        return make_response("Enter the course code of the course you want to apply to",200)
    
    course_code = request.form.get('courseCode')
    student_id = request.form.get('stud_id')
    lecturer_id = request.form.get('lect_id')

    
    if not course_code:
        return make_response({"Status": "Please provide a course code."}, 400)

    # check if the course exists
    course = dbm.get_courses(course_code)
    if course is None:
        return make_response({"Status": "Course not found."}, 404)
    
    lect,studs = dbm.get_members(course_code)

    # check if a lecturer is already assigned to the course
    if len(lect) != 0:
        return make_response({"Status": "A lecturer is already assigned to this course."}, 400)

        
    # if the lecturer ID is provided, check if it is valid
    if lecturer_id:
        lecturer = dbm.get_lecturer_by_id(lecturer_id)
        if not lecturer:
            return make_response({"Status": "Invalid lecturer ID."}, 400)
        course['lect_id'] = lecturer_id

    # if the student ID is provided, register the student for the course
    if student_id:
        student = dbm.get_student_by_id(student_id)
        if not student:
            return make_response({"Status": "Invalid student ID."}, 400)
        # check if the student is already registered for the course
        if dbm.is_enrolled(course_code, student_id):
            return make_response({"Status": "Student already registered for the course."}, 400)
        dbm.enroll_student_in_course(course_code, student_id)

    # update the course in the database
    dbm.update_course(course)

    return make_response({"Status": "Registration successful."}, 200)

@app.route('/courses/<courseCode>/events', methods=['GET','POST'])
def CalendarEvents(courseCode):
    if not session.get('userType'):
        return make_response("Login to view course events",404)
    
    if request.method == "GET":
        events = dbm.get_course_events(courseCode)
        if events is not None:
            return make_response(events, 200)
        
        return make_response({"Status": "No calendar events found for this course."}, 404)
    
    if session['userType'] != "ADMIN":
        return make_response("Only admins can access this page and you are not one.", 404)
    
    event_title = request.form.get('eventTitle')
    event_date = request.form.get('eventDate')
    event_details = request.form.get('eventDetails')
    
    isCourse = dbm.get_courses(courseCode)
    if isCourse is None:
        return make_response("That Course does not exist.",404)
    
    dbm.create_calendar_event({"courseCode": courseCode, "event_title": event_title, "event_date": event_date, "event_details": event_details})

    return make_response({"Status": "Event created successfully."}, 200)

@app.route('/events', methods=['GET','POST'])
def getStudentCalendarEvents(stud_id):
    if not session.get('userType'):
        return make_response("Login to view student calendar events",404)
    
    if request.method == 'GET':
        return make_response("Enter the date you wish to view events for.")
    
    date = request.form.get('date')
    events
    
    if session['userType'] == "STUDENT":
        if not date:
            return make_response({"Status": "Please provide a date."}, 404)

        events = dbm.get_date_events(date, session['userID'])
        
    else:
        stud_id = request.form.get('stud_id')
        events = dbm.get_date_events(date, stud_id)
        
    if events is not None:
        return make_response(events, 200)
    else:
        return make_response({"Status": "No calendar events found for this student on this date."}, 404)

@app.route('/courses/<courseCode>/events', methods=['POST'])
def createCalendarEvent(courseCode):
    if not session.get('userType'):
        return make_response("Login to create calendar events.",404)
    
    event_title = request.form.get('eventTitle')
    event_date = request.form.get('eventDate')
    event_details = request.form.get('eventDetails')

    if session['userType'] == 'ADMIN':
        dbm.create_calendar_event({"courseCode": courseCode, "event_name": event_title, "event_date": event_date, "event_details": event_details})

        return make_response({"Status": "Event created successfully."}, 200)
    else:
        return make_response({"Status": "You do not have permission to create an event."}, 401)

@app.route('/reports', methods=['POST'])
def getReports():
    if not session.get('userType'):
        return make_response("Login to view reports",404)
    
    report_type = request.form.get('type')

    if report_type == 'courses_50_or_more_students':
        courses = dbm.get_courses_with_50_or_more_students()
        return make_response(courses, 200)
    elif report_type == 'students_5_or_more_courses':
        students = dbm.get_students_with_5_or_more_courses()
        return make_response(students, 200)
    elif report_type == 'lecturers_3_or_more_courses':
        lecturers = dbm.get_lecturers_with_3_or_more_courses()
        return make_response(lecturers, 200)
    elif report_type == 'top_10_enrolled_courses':
        courses = dbm.get_top_10_enrolled_courses()
        return make_response(courses, 200)
    elif report_type == 'top_10_students_highest_averages':
        students = dbm.get_top_10_students_highest_averages()
        return make_response(students, 200)
    else:
        return make_response({"Status": "Invalid report type."}, 400)
    
@app.route('/Forums/<course>',methods=['GET'])
def getForums(course):
    if not session.get('userType'):
        return make_response("Login to view forums",404)
    
    forums = dbm.get_forums(course)
    return make_response(forums)

@app.route('/CourseMembers/<course>',methods=['GET'])
def getCourseMembers(course):
    if not session.get('userType'):
        return make_response("Login to view course members",404)
    
    members = dbm.get_members(course)
    
    if members is None:
        return make_response("That course does not exist",404)
    
    return make_response(members,200)

if __name__ == "__main__": 
    #sql_gen.genCreateSQL()
    #sql_gen.genInsertSQL()
    #sql_gen.executeSQL()
    app.run()
    