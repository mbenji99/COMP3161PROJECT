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
    else:
        # retrieve all courses
        courses = dbm.get_all_courses()
        return make_response(courses, 200)

if __name__ == "__main__":
    dbm.create_tables()
    dbm.populate_tables()
    #app.run()
    

'''
CREATE TABLE Forums(
    forumID int PRIMARY KEY,
    forumTitle varchar(200),
    forumDetails varchar(200),
    courseCode varchar(50),
    dateCreated date,
    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));

CREATE TABLE Threads(
    threadID int PRIMARY KEY,
    userID int,
    forumID int,
    threadDetails varchar(255),
    replyID int,
    dateCreated date,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (forumID) REFERENCES Forums(forumID));
'''