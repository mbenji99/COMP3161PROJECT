from flask import Flask, jsonify,make_response,request,session,render_template,redirect,url_for
from flask_login import LoginManager
from werkzeug.utils import secure_filename
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
    if not session.get('userType'):        
        return render_template('home.html',
                           userType='VISITOR')
    return render_template('home.html',
                        userType=session['userType'])

# REGISTER
@app.route('/register',methods=['GET','POST'])
def register():
    if not session.get('userType'):
        form = forms.RegistrationForm()
        return render_template('registration.html',
                            form=form,
                            userType='VISITOR')
        
    if request.method == "GET":
        form = forms.RegistrationForm()
        return render_template('registration.html',
                            form=form,
                            userType=session['userType'])
        
    userID = request.form.get('userID')
    passW = request.form.get('password')
    fName= request.form.get('first_name')
    lName= request.form.get('last_name')
    userType = request.form.get('account_type')
    email = request.form.get('email')
    
   
    if userID[:3] == "620" and len(userID) <= 9:
        res = dbm.register_user({"userID":userID,"passW":passW,"userType":userType,"fName":fName,"lName":lName,"email":email})
        
        if res == 1:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    return redirect(url_for('register'))

# LOGIN
@app.route('/login',methods=['POST','GET'])
def login():
        
    if request.method == "GET":
        form = forms.LoginForm()
        return render_template('login.html',
                            form=form)
    
    userID = request.form.get('username')
    passW = request.form.get('password')
    
   
    res = dbm.login_user(userID,passW)
    
    if res is None:
        return redirect(url_for('login'))
    
    session['userType'] = res
    session['userID'] = userID
    return render_template('home.html',
                           userType=session['userType'])

# LOGOUT
@app.route('/logout')
def logout():
    if not session.get('userType'):
        return make_response("Go to /login to login.",404)
    session.pop('userType')  
    session.pop('userID')
    return redirect(url_for('login'))

@app.route('/create_course', methods=['POST','GET'])
def createCourse():
    if not session.get('userType'):
        return make_response("Login to create courses",404)
    
    if session['userType'] != "ADMIN":
        return make_response("Only admins can access this page and you are not one.", 404)
    
    if request.method == 'GET':
        ccForm = forms.CreateCourse()
        return render_template('create_course.html',
                                form=ccForm,
                                userType=session['userType'])
    
    
    courseCode = request.form.get("courseCode")
    course_name = request.form.get('course_name')
    start_date = request.form.get('start_date')
    credits = request.form.get('credits')
    
    if courseCode is None or course_name is None or start_date is None or credits is None:
        return make_response("Please ensure there is something in all fields before submitting",404)

    dbm.create_course({"courseCode": courseCode, "course_name": course_name, "start_date": start_date, "credits": credits})

    return make_response({"Status": "Course created successfully.", "courseCode": courseCode}, 200)
  
# COURSES 
@app.route('/courses',methods=['GET','POST'])
def get_courses():
    if not session.get('userType'):
        return make_response("Login to view courses",404)
    
    cForm = forms.Courses()
    if request.method == "GET":
        courses = dbm.get_courses("All")
        if session['userType'] != "ADMIN":
            courses = dbm.get_courses_by_id(session['userID'])
        return render_template('view_courses.html',
                                form=cForm,
                                all_course=courses,
                                userType=session['userType'])

    u_id = request.form.get('u_id')
    courses = dbm.get_courses_by_id(u_id)
    
    if courses is not None:
        return render_template('view_courses.html',
                                form=cForm,
                                all_course=courses,
                                userType=session['userType'])
    
    return make_response("That id does not exist or is not registered for any course",404)
        
   
@app.route('/register_course', methods=['GET','POST'])
def register_course():
    if not session.get('userType'):
        return make_response("Login to register for courses",404)
    
    if request.method == "GET":
        rForm = forms.CourseRegistration()
        courses = dbm.get_courses("All")
        return render_template('register_for_course.html',
                                form=rForm,
                                all_course=courses,
                                userType=session['userType'])
    
    course_code = request.form.get('courseCode') 
    
    # check if the course exists
    course = dbm.get_courses(course_code)
    if course is None:
        return make_response({"Status": "Course not found."}, 404)
    
    
    regCourses = dbm.get_courses_by_id(session['userID'])
    isRegistered = False
    if regCourses is not None:
        for rCourse in regCourses:
            if course_code == rCourse['courseCode']:
                isRegistered = True
                break


    # check if a lecturer is already assigned to the course
    if isRegistered and session['userType'] == "LECTURER":
        return make_response({"Status": "A lecturer is already assigned to this course."}, 400)

    elif isRegistered and session['userType'] == "STUDENT":
        return make_response({"Status": "You are already registered for this course."}, 400)
        
    res = dbm.register_for_course(session['userID'],course_code)
    
    if res == 0:
        return make_response("Cannot register for any more courses",404)

    return make_response({"Status": "Registration successful."}, 200)

# REGISTER COURSE
@app.route('/members/<course>',methods=['GET'])
def getCourseMembers(course):
    if not session.get('userType'):
        return make_response("Login to view course members",404)
    
    if course == "search":
        courses = dbm.get_courses("All")
        return render_template('members.html',all_course=courses)
    
    members = dbm.get_members(course)
    
    if members is None:
        return make_response("That course does not exist",404)
    
    return render_template('courseMembers.html',students=members[1],lecturer=members[0],cc=course)

# CALENDAR EVENTS
@app.route('/events', methods=['GET','POST'])
def CalendarEvents():
    if not session.get('userType'):
        return make_response("Login to view student calendar events",404)
    
    eForm = forms.getCalendarEvents()
    
    if request.method == 'GET':
        if session['userType'] != "ADMIN":
            courses = dbm.get_courses_by_id(session['userID'])
            return render_template("calendar_events.html",
                               userType=session['userType'],
                               form=eForm,
                               courses=courses)
        else:
            return render_template("calendar_events.html",
                               userType=session['userType'],
                               form=eForm)
    
    form_type = request.form.get("formType")
    courses=""
    if session['userType'] != "ADMIN":
            courses = dbm.get_courses_by_id(session['userID'])
    
    match form_type:
        case "search_by_course":
            course = request.form.get('courseCode')
            
            events = dbm.get_course_events(course)
            
            
            if events is not None:
                return render_template('calendar_events.html',
                                        userType=session['userType'],
                                        form=eForm,
                                        events=events,
                                        courses=courses)
            
            return render_template('calendar_events.html',
                                    userType=session['userType'],
                                    form=eForm,
                                    courses=courses)
        case "search_by_stud_id":
            date = request.form.get('date')
            
            if session['userType'] != "STUDENT":
                stud_id = request.form.get('stud_id')
                events = dbm.get_date_events(date, stud_id)
            else:
                events = dbm.get_date_events(date, session["userID"])
             
            if events is not None:
                return render_template('calendar_events.html',
                                        userType=session['userType'],
                                        form=eForm,
                                        events=events,
                                        courses=courses)
            
            return render_template('calendar_events.html',
                                    userType=session['userType'],
                                    form=eForm,
                                    courses=courses)
        case "create_course":
            date = request.form.get('date')
            course = request.form.get('courseCode')
            name = request.form.get('name')
            details = request.form.get('details')
            dbm.create_calendar_event({
                "event_name":name,
                "courseCode":course,
                "event_details":details,
                "event_date":date
            })
            
            return render_template('calendar_events.html',
                                    userType=session['userType'],
                                    form=eForm,
                                    courses=courses)
    
# FORUMS AND THREADS
@app.route('/forums', methods=['POST'])
def create_forum():
    data = request.get_json()
    forum_id = data['forum_id']
    forum_title = data['forum_title']
    forum_details = data['forum_details']
    courseCode = data['courseCode']
    date_created = data['date_created']
    create_forum(forum_id, forum_title, forum_details, courseCode, date_created)
    return jsonify({'message': 'Forum created successfully!'})

# Create a new thread
@app.route('/threads', methods=['POST'])
def create_thread():
    data = request.get_json()
    thread_id = data['thread_id']
    u_id = data['u_id']
    forum_id = data['forum_id']
    thread_details = data['thread_details']
    reply_id = data['reply_id']
    date_created = data['date_created']
    create_thread(thread_id, u_id, forum_id, thread_details, reply_id, date_created)
    return jsonify({'message': 'Thread created successfully!'})

# Get all threads for a forum
@app.route('/forums/<int:forum_id>/threads', methods=['GET'])
def get_forum_threads(forum_id):
    threads = get_forum_threads(forum_id)
    return jsonify({'threads': threads})

# Get all posts for a thread
@app.route('/threads/<int:thread_id>/posts', methods=['GET'])
def get_thread_posts(thread_id):
    posts = get_thread_posts(thread_id)
    return jsonify({'posts': posts})

@app.route('/posts', methods=['POST'])
def create_post_api():
    data = request.get_json()
    post_id = data['post_id']
    u_id = data['u_id']
    thread_id = data['thread_id']
    post_details = data['post_details']
    date_created = data['date_created']
    dbm.create_post(post_id, u_id, thread_id, post_details, date_created)
    return jsonify({'message': 'Post created successfully!'})

# COURSE CONTENT AND SECTIONS
@app.route('/content/<courseCode>',methods=['GET'])
def content(courseCode):
    if not session.get('userType'):
        return make_response("Login to view courses",404)
    
    isvalidCourse = dbm.get_courses(courseCode)
    
    if isvalidCourse is None:
        return make_response("That is not a valid course.",404)
    
    contents= dbm.get_course_content(courseCode)
    sections = dbm.get_sections(courseCode)
    assignments = dbm.get_assignments(courseCode)
    notAssignments = []
    
    isAssignment = False
    for content in contents:
        for assignment in assignments:
            if content[0] == assignment[1]:
                isAssignment = True
        if not isAssignment:
            notAssignments.append(content)
        isAssignment = False
    
    return render_template('content.html',
                           userType=session['userType'],
                           sections=sections,
                           contents=notAssignments,
                           cc=courseCode,
                           assignments=assignments)

@app.route('/add_section/<courseCode>', methods=['GET','POST'])
def addSection(courseCode):
    if not session.get('userType'):
        return make_response("Login to add course section",404)
    elif session['userType'] == "STUDENT":
        return make_response("You need to be a Lecturer to add section.")
    elif request.method == 'GET':
        sections = dbm.get_sections(courseCode)
        if sections is None:
            return make_response("That course does not exist.",404)
        sForm = forms.Sections()
        return render_template('add_sections.html',sections=sections,cc=courseCode,form=sForm)

    section_name = request.form.get('section_name')
    dbm.add_section([courseCode,section_name])
    return redirect(url_for('content',courseCode=courseCode))
 
@app.route('/add_content/<courseCode>', methods=['GET','POST'])
def addContent(courseCode):
    if not session.get('userType'):
        return make_response("Login to add course content",404)
    elif session['userType'] == "STUDENT":
        return make_response("You need to be a Lecturer to add content.")
    elif request.method == 'GET':
        sections = dbm.get_sections(courseCode)
        cForm = forms.Content()
        return render_template('add_content.html',form=cForm,sections=sections,cc=courseCode)

    section_id = request.form.get('section_id')
    details = request.form.get('details')
    file = request.files['file']
    file_name = secure_filename(file.filename)
    
    dbm.add_course_content([section_id,details,file_name])
    
    sections = dbm.get_sections(courseCode)
    cForm = forms.Content()
    return render_template('add_content.html',form=cForm,sections=sections,cc=courseCode)

# ASSIGNMENTS
@app.route('/add_assignment/<courseCode>',methods=['GET','POST'])
def addAssignment(courseCode):
    if not session.get('userType'):
        return make_response("Login to add assignments",404)
    elif session['userType'] == "STUDENT":
        return make_response("Only Lecturers and Admins can add assignments",404)
    
    if request.method == "GET":
        aForm = forms.CreateAssignment()
        sections = dbm.get_sections(courseCode)
        return render_template("add_assignment.html",
                               form=aForm,
                               cc=courseCode,
                               sections=sections,
                               userType=session['userType'])
        
    
    section_id = request.form.get("section_id")
    details = request.form.get("details")
    due_date = request.form.get("due_date")
    file = request.files['file']
    file_name = secure_filename(file.filename)
    
    dbm.add_assignment([section_id,due_date,details,file_name])
    
    return redirect(url_for("addAssignment",courseCode=courseCode))


@app.route('/submit_assignment/<assignmentID>',methods=['GET','POST'])
def submitAssignment(assignmentID):
    if not session.get('userType'):
        return make_response("Login to view courses",404)
    
    if request.method == "GET":
        assignmentInfo = dbm.get_assignment(assignmentID)
        print(assignmentInfo)
        aForm = forms.SubmitAssignment()
        return render_template('submit_assignment.html',
                               userType=session['userType'],
                               info=assignmentInfo,
                               form=aForm)
        
    file = request.files['file']
    file_name = secure_filename(file.filename)
    
    dbm.submit_assignment([file_name,assignmentID,session['userID']])
      
# REPORTS
@app.route('/reports', methods=['GET','POST'])
def getReports():
    if not session.get('userType'):
        return make_response("Login to view reports",404)
    
    if request.method == 'GET':
        rForm = forms.Reports()
        return render_template('reports.html',form=rForm)
    
    report_type = request.form.get('report_type')

    if report_type == 'courses_50_or_more_students':
        courses = dbm.get_courses_with_50_or_more_students()
        return render_template("50ormore.html",all_course=courses)
    elif report_type == 'students_5_or_more_courses':
        students = dbm.get_students_with_5_or_more_courses()
        return render_template("5ormore.html",all_course=students)
    elif report_type == 'lecturers_3_or_more_courses':
        lecturers = dbm.get_lecturers_with_3_or_more_courses()
        return render_template("3ormorecourses.html",all_course=lecturers)
    elif report_type == 'top_10_enrolled_courses':
        courses = dbm.get_top_10_enrolled_courses()
        return render_template("10mostcourses.html",all_course=courses)
    elif report_type == 'top_10_students_highest_averages':
        students = dbm.get_top_10_students_highest_averages()
        return make_response(students, 200)
    else:
        return make_response({"Status": "Invalid report type."}, 400)


if __name__ == "__main__": 
    app.run()
    