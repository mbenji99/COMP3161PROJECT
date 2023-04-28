from flask import Flask,make_response,request
import DBManager as dbm

app = Flask(__name__)

@app.route('/')
def index():
    return make_response({"Course":"COMP3161 - Intro to Database Management Systems"},200)

@app.route('/register',methods=['GET','POST'])
def register():
    userID = request.form.get('userID')
    passW = request.form.get('passW')
    fName= request.form.get('fName')
    lName= request.form.get('lName')
    userType = request.form.get('userType')
    userID = str(userID)
    
    if userID[:3] == "620" and len(userID) <= 9:
        dbm.register_user({"userID":userID,"passW":passW,"userType":userType,"fName":fName,"lName":lName})
        return make_response({"Status":"Success"},200)
    else:
        return make_response({"Status": "Invalid user id."},404)

  
@app.route('/users',methods=['GET'])
def getUsers():
    db = dbm.get_database()
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    
    users = []
    
    for uid,fn,ln,email,passw in cursor:
        user = {}
        user['UserID'] = uid
        user['FirstName'] = fn
        user['LastName'] = ln
        user['Email'] = email
        user['Password'] = passw
        users.append(user)
        
        
    cursor.close()
    db.close()
    return make_response(users,200)

@app.route('/courses', methods=['POST'])
def createCourse():
    admin_user_type = "admin"
    userID = request.form.get('userID')
    passW = request.form.get('passW')
    course_name = request.form.get('courseName')
    start_date = request.form.get('startDate')

    # check if the user is an admin
    user = dbm.get_user_by_id(userID)
    if user and user['passW'] == passW and user['userType'] == admin_user_type:
        # generate a new course ID
        c_id = "C" + str(dbm.get_next_course_id())

        # insert the new course into the database
        dbm.create_course({"c_id": c_id, "course_name": course_name, "start_date": start_date})

        return make_response({"Status": "Course created successfully.", "c_id": c_id}, 200)
    else:
        return make_response({"Status": "You do not have permission to create a course."}, 401)


@app.route('/courses', methods=['GET'])
def getCourses():
    course_id = request.args.get('courseID')
    student_id = request.args.get('studentID')
    lecturer_id = request.args.get('lecturerID')

    if not any([course_id, student_id, lecturer_id]):
        return make_response({"Status": "Please provide a query parameter to retrieve courses."}, 400)

    if course_id:
        # retrieve a specific course
        course = dbm.get_course_by_id(course_id)
        if course:
            return make_response(course, 200)
        else:
            return make_response({"Status": "Course not found."}, 404)
    elif student_id:
        # retrieve courses for a specific student
        courses = dbm.get_courses_by_student_id(student_id)
        return make_response(courses, 200)
    elif lecturer_id:
        # retrieve courses taught by a specific lecturer
        courses = dbm.get_courses_by_lecturer_id(lecturer_id)
        return make_response(courses, 200)

@app.route('/register_course', methods=['POST'])
def registerCourse():
    course_id = request.form.get('courseID')
    student_id = request.form.get('studentID')
    lecturer_id = request.form.get('lecturerID')

    if not course_id:
        return make_response({"Status": "Please provide a course ID."}, 400)

    # check if the course exists
    course = dbm.get_course_by_id(course_id)
    if not course:
        return make_response({"Status": "Course not found."}, 404)

    # check if a lecturer is already assigned to the course
    if course['lecturerID']:
        return make_response({"Status": "A lecturer is already assigned to this course."}, 400)

    # if the lecturer ID is provided, check if it is valid
    if lecturer_id:
        lecturer = dbm.get_user_by_id(lecturer_id)
        if not lecturer or lecturer['userType'] != 'lecturer':
            return make_response({"Status": "Invalid lecturer ID."}, 400)
        course['lecturerID'] = lecturer_id

    # if the student ID is provided, register the student for the course
    if student_id:
        student = dbm.get_user_by_id(student_id)
        if not student or student['userType'] != 'student':
            return make_response({"Status": "Invalid student ID."}, 400)
        # check if the student is already registered for the course
        if dbm.is_registered(course_id, student_id):
            return make_response({"Status": "Student already registered for the course."}, 400)
        dbm.register_student_for_course(course_id, student_id)

    # update the course in the database
    dbm.update_course(course)

    return make_response({"Status": "Registration successful."}, 200)

@app.route('/courses/<course_id>/events', methods=['GET'])
def getCalendarEvents(course_id):
    events = dbm.get_events_by_course_id(course_id)
    if events:
        return make_response(events, 200)
    else:
        return make_response({"Status": "No calendar events found for this course."}, 404)

@app.route('/students/<student_id>/events', methods=['GET'])
def getStudentCalendarEvents(student_id):
    date = request.args.get('date')
    if not date:
        return make_response({"Status": "Please provide a date query parameter."}, 400)

    events = dbm.get_events_by_student_id_and_date(student_id, date)
    if events:
        return make_response(events, 200)
    else:
        return make_response({"Status": "No calendar events found for this student on this date."}, 404)

@app.route('/courses/<course_id>/events', methods=['POST'])
def createCalendarEvent(course_id):
    admin_user_type = "admin"
    userID = request.form.get('userID')
    passW = request.form.get('passW')
    event_name = request.form.get('eventName')
    event_date = request.form.get('eventDate')
    event_desc = request.form.get('eventDescription')

    # check if the user is an admin
    user = dbm.get_user_by_id(userID)
    if user and user['passW'] == passW and user['userType'] == admin_user_type:
        # generate a new event ID
        e_id = "E" + str(dbm.get_next_event_id())

        # insert the new event into the database
        dbm.create_event({"e_id": e_id, "course_id": course_id, "event_name": event_name, "event_date": event_date, "event_desc": event_desc})

        return make_response({"Status": "Event created successfully.", "e_id": e_id}, 200)
    else:
        return make_response({"Status": "You do not have permission to create an event."}, 401)

@app.route('/reports', methods=['GET'])
def getReports():
    report_type = request.args.get('type')

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
if __name__ == "__main__":
    dbm.genCreateSQL()
    dbm.genInsertSQL()


