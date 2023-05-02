import mysql.connector
from datetime import datetime

USER,PASS = "root","UltimaPass420"
HOST,DB = "localhost","eclass"
AUTH = "mysql_native_password"

# Helper Functions

def get_database():
    db = mysql.connector.connect(
        user=USER,password=PASS,
        host=HOST,database=DB,
        auth_plugin=AUTH)
    return db

def getUserType(id):
    db = get_database()
    cursor = db.cursor()
    
    query = f"SELECT * FROM Admins WHERE admin_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        print("admin")
        return "ADMIN"
    
    query = f"SELECT * FROM Students WHERE stud_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        return "STUDENT"
    
    query = f"SELECT * FROM Lecturers WHERE lect_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        print("lecturer")
        return "LECTURER"
    
    cursor.close()
    db.close()

def get_user_course_number(uid,uType):
    db = get_database()
    cursor = db.cursor()
    query = ""
    if uType == "STUD":
        query = f"SELECT courseCode FROM Enrolled WHERE u_id = {uid}"
    else:
        query = f"SELECT courseCode FROM Course_Maintainers WHERE lect_id = {uid}"
    
    cursor.execute(query)
    res = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return res

# REGISTER USER

def register_user(info):
    db = get_database()
    cursor = db.cursor()
    
    userID,passW,userType = info['userID'],info['passW'],info['userType']
    fName,lName = info['fName'],info['lName']
    
    # Check if userID already exists
    query = f"SELECT * FROM Users WHERE u_id = {userID}"
    cursor.execute(query)
    res = cursor.fetchone()
    
    if res is not None:
        return 0
    
    # If unused, insert into table
    query = f"INSERT INTO Users (u_id, fName, lName, email, passW) VALUES "
    query += f"({userID},'{fName}','{lName}','{fName}{lName}@gmail.com','{passW}')"
    cursor.execute(query)
    
    if userType == "STUDENT":
        query = "INSERT INTO Students (stud_id,level,date_enrolled) VALUES "
        query += f"({userID},'UNDERGRAD', CURRENT_DATE())"
    elif userType == "LECTURER":
        query = "INSERT INTO Lecturers (lect_id,salary) VALUES "
        query += f"({userID},80000)"
    cursor.execute(query)
    
    db.commit()
    
    cursor.close()
    db.close()
    return 1

# LOGIN USER

def login_user(userID, passW):
    db = get_database()
    cursor = db.cursor()
    
    query = f"SELECT * FROM Users WHERE u_id = {userID} AND passW = '{passW}'"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        return getUserType(userID)
    
    return 

# COURSES

def create_course(info):
    # Create a new course with the provided information
    db = get_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Courses (courseCode, course_name, start_date, credits) VALUES (%s, %s, %s, %s)",
                   (info['courseCode'], info['course_name'], info['start_date'], info['credits']))
    db.commit()
    
    cursor.close()
    db.close()
    
def get_courses(case):
    db = get_database()
    cursor = db.cursor(dictionary=True)
    output = None
    if case == "All":
        cursor.execute("SELECT * FROM Courses")
        output = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Courses WHERE courseCode=%s", (case,))
        output = cursor.fetchall()
    
    cursor.close()
    db.close()
    return output

def get_courses_by_id(id):
    db = get_database()
    cursor = db.cursor(dictionary=True)
    
    userType = getUserType(id)
    query = ""
    
    if userType == "LECTURER":
        query = f"SELECT Courses.courseCode,Courses.course_name,Courses.start_date,Courses.credits FROM Course_Maintainers JOIN Courses ON Course_Maintainers.courseCode = Courses.courseCode WHERE Course_Maintainers.lect_id = {id}"
    elif userType == "STUDENT":
        query = f"SELECT Courses.courseCode,Courses.course_name,Courses.start_date,Courses.credits FROM Enrolled JOIN Courses ON Enrolled.courseCode = Courses.courseCode WHERE Enrolled.u_id = {id}"
    else:
        return
    
    cursor.execute(query)
    res = cursor.fetchall()
    
    cursor.close()
    db.close()
    return res

def register_for_course(uid,cc):
    uType = getUserType(uid)
    db = get_database()
    cursor = db.cursor()
    query = ""
    
    if uType == 'STUDENT':
        courses = get_user_course_number(uid,'STUD')
        if len(courses) >= 6 or cc in courses:
            return 0
        query = f"INSERT INTO Enrolled (u_id, courseCode) VALUES ({uid}, '{cc}')"
    
    else:
        courses = get_user_course_number(uid,'LECT')
        if len(courses) >= 5 or cc in courses:
            return 0
        query = f"INSERT INTO Course_Maintainers (lect_id, courseCode) VALUES ({uid}, '{cc}')"
                    

    cursor.execute(query)
    db.commit()
    
    cursor.close()
    db.close()
    return 1

# MEMBERS

def get_members(course):
    db = get_database()
    cursor = db.cursor()
    
    c_query = f"SELECT * FROM Courses WHERE courseCode = '{course}'"
    cursor.execute(c_query)
    res = cursor.fetchone()
    
    if res is None:
        return
    
    stud_query = f"SELECT Users.u_id, Users.fName, Users.lName FROM Enrolled JOIN Users ON Enrolled.u_id = Users.u_id WHERE courseCode = '{course}' ORDER BY Users.fName"
    cursor.execute(stud_query)
    students = cursor.fetchall()
    
    lect_query = f"SELECT Users.u_id, Users.fName, Users.lName FROM Course_Maintainers JOIN Users ON Course_Maintainers.lect_id = Users.u_id WHERE courseCode = '{course}'"
    cursor.execute(lect_query)
    lecturer = cursor.fetchone()
    
    cursor.close()
    db.close()
    return [lecturer,students]

# CALENDAR EVENTS
def create_calendar_event(info):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO CalendarEvents (event_name, courseCode, event_details, event_date) \
                    VALUES (%s, %s, %s, %s)", (info['event_name'], info['courseCode'], info['event_details'], info['event_date']))
    db.commit()
    
    cursor.close()
    db.close()

def create_assignment_event(info):
    db = get_database()
    cursor = db.cursor()
    
    calInfo = {
        "event_name":info['event_name'],
        "courseCode":info['courseCode'],
        "event_details":info['event_details'],
        "event_date":info['event_date']
    }
    create_calendar_event(calInfo)
    
    query = "SELECT * FROM CalendarEvents ORDER BY event_id DESC LIMIT 1"
    cursor.execute(query)
    res = cursor.fetchone()
    assignID = info['assignment_id']
    
    query = f"INSERT INTO AssignmentEvents (event_id,assignment_id) VALUES ({res[0]},{assignID})"
    cursor.execute(query)
    db.commit()
    
    cursor.close()
    db.close()   
    
def get_course_events(course_code):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM CalendarEvents WHERE courseCode=%s", (course_code,))
    
    res = cursor.fetchall()
    cursor.close()
    db.close()
    
    return res

def get_date_events(date, student_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM CalendarEvents WHERE event_date ='{date}' AND courseCode IN (SELECT courseCode FROM Enrolled WHERE u_id={student_id})")
    
    res = cursor.fetchall()
    cursor.close()
    db.close()
    
    return res

# FORUMS AND THREADS

def create_forum(forum_id, forum_title, forum_details, courseCode, date_created):
    # insert new forum into Forums table
    db = get_database()
    cursor = db.cursor()
    query = "INSERT INTO Forums (forum_id, forum_title, forum_details, courseCode, date_created) VALUES (%s, %s, %s, %s, %s)"
    values = (forum_id, forum_title, forum_details, courseCode, date_created)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

def create_thread(thread_id, u_id, forum_id, thread_details, reply_id, date_created):
    # insert new thread into Threads table
    db = get_database()
    cursor = db.cursor()
    query = "INSERT INTO Threads (thread_id, u_id, forum_id, thread_details, reply_id, date_created) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (thread_id, u_id, forum_id, thread_details, reply_id, date_created)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

def get_forum_threads(forum_id):
    # select all threads for the given forum_id
    db = get_database()
    cursor = db.cursor()
    query = "SELECT * FROM Threads WHERE forum_id = %s"
    values = (forum_id,)
    cursor.execute(query, values)

    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res

def get_thread_posts(thread_id):
    # select all posts for the given thread_id
    db = get_database()
    cursor = db.cursor()
    query = "SELECT * FROM Posts WHERE thread_id = %s"
    values = (thread_id,)
    cursor.execute(query, values)

    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res

def create_post(post_id, u_id, thread_id, post_details, date_created):
    # insert new post into Posts table
    db = get_database()
    cursor = db.cursor()
    query = "INSERT INTO Posts (post_id, u_id, thread_id, post_details, date_created) VALUES (%s, %s, %s, %s, %s)"
    values = (post_id, u_id, thread_id, post_details, date_created)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()
    
# COURSE CONTENT AND SECTIONS
    
def add_section(info):
    db = get_database()
    cursor = db.cursor()
    
    query = f"INSERT INTO Sections (courseCode,section_name) VALUES ('{info[0]}','{info[1]}')"
    cursor.execute(query)
    
    db.commit()
    cursor.close()
    db.close()

def get_sections(courseCode):
    db = get_database()
    cursor = db.cursor()
    
    query = f"SELECT * FROM Sections WHERE courseCode = '{courseCode}'"
    cursor.execute(query)
    sections = cursor.fetchall()
    
    cursor.close()
    db.close()
    return sections
        
def add_course_content(info):
    db = get_database()
    cursor = db.cursor()
    
    query = f'INSERT INTO Content (section_id,details,file_name) VALUES ({info[0]},"{info[1]}","{info[2]}")'
    cursor.execute(query)
    
    db.commit()
    cursor.close()
    db.close()

def get_course_content(courseCode):
    db = get_database()
    cursor = db.cursor()
    
    sections = get_sections(courseCode)
    allContent = []
    
    if sections is None:
        return
    
    for section in sections:
        query = f"SELECT * FROM Content WHERE section_id = {section[0]}"
        cursor.execute(query)
        content = cursor.fetchall()
        if content is None:
            continue
        for c in content:
            allContent.append(c)
        
        
    
    cursor.close()
    db.close()
    return allContent

# ASSIGNMENTS

def add_assignment(info):
    section_id = info[0]
    due_date = info[1]
    details = info[2]
    file_name = info[3]
    
    db = get_database()
    cursor = db.cursor()
    
    add_course_content([section_id,details,file_name])
    
    query = "SELECT * FROM Content ORDER BY content_id DESC LIMIT 1"
    cursor.execute(query)
    res = cursor.fetchone()
    assign_id = res[0]
    
    query = f"INSERT INTO Assignments (assignment_id,due_date) VALUES ({res[0]},'{due_date}')"
    cursor.execute(query)
    db.commit()
    
    query = f"SELECT * FROM Sections WHERE section_id = {section_id}"
    cursor.execute(query)
    res = cursor.fetchone()
    
    event_info = {
        "assignment_id":assign_id,
        "event_name":details,
        "courseCode":res[1],
        "event_details":file_name,
        "event_date":due_date
    }
    
    create_assignment_event(event_info)
    
    cursor.close()
    db.close()
    
def get_assignments(courseCode):
    db = get_database()
    cursor = db.cursor()
    
    query = f'''SELECT Sections.section_id,Content.content_id,Content.details,Content.file_name,Assignments.due_date \
                FROM Sections \
                JOIN Content ON Sections.section_id=Content.section_id \
                JOIN Assignments ON Content.content_id=Assignments.assignment_id \
                WHERE Sections.courseCode = "{courseCode}"'''
    cursor.execute(query)
    assignments = cursor.fetchall()
    
    cursor.close()
    db.close()
    return assignments

def get_assignment(assign_id):
    db = get_database()
    cursor = db.cursor()
    
    query = f'''SELECT Sections.section_id,Content.content_id,Content.details,Content.file_name,Assignments.due_date \
                FROM Sections JOIN Content ON Sections.section_id=Content.section_id \
                JOIN Assignments ON Content.content_id=Assignments.assignment_id \
                WHERE Content.content_id = {assign_id}'''
    print(assign_id)
    cursor.execute(query)
    assignments = cursor.fetchone()
    
    cursor.close()
    db.close()
    return assignments
    
def submit_assignment(info):
    db = get_database()
    cursor = db.cursor()
    dateN = datetime.date()
    
    query = f"INSERT INTO Submissions (assignment_id,stud_id,file_name,date_submitted) VALUES \
            ({info[1]},{info[2]},'{info[0]}',{dateN})"
    cursor.execute(query)
    
    cursor.close()
    db.close()
    
# REPORTS

def get_courses_with_50_or_more_students():
    db = get_database()
    query = """
        SELECT c.courseCode, c.course_name, COUNT(e.u_id) as num_students
        FROM Courses c
        JOIN Enrolled e ON c.courseCode = e.courseCode
        GROUP BY c.courseCode
        HAVING COUNT(e.u_id) >= 50
        ORDER BY num_students DESC;
    """
    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()
    db.close()
    
    return result

def get_students_with_5_or_more_courses():
    db = get_database()
    query = """
        SELECT Students.stud_id, Users.fName, Users.lName, COUNT(Enrolled.courseCode) as num_courses
        FROM Students
        JOIN Enrolled ON Students.stud_id = Enrolled.u_id
        JOIN Users ON Students.stud_id = Users.u_id
        GROUP BY Students.stud_id
        HAVING COUNT(Enrolled.courseCode) >= 5
        ORDER BY num_courses DESC;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    cursor.close()
    db.close()
    return result

def get_lecturers_with_3_or_more_courses():
    db = get_database()
    query = """
        SELECT Lecturers.lect_id, Users.fName, Users.lName, COUNT(Course_Maintainers.courseCode) as num_courses
        FROM Lecturers
        JOIN Course_Maintainers ON Lecturers.lect_id = Course_Maintainers.lect_id
        JOIN Users ON Lecturers.lect_id = Users.u_id
        GROUP BY Lecturers.lect_id
        HAVING COUNT(Course_Maintainers.courseCode) >= 3
        ORDER BY num_courses DESC;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def get_top_10_enrolled_courses():
    db = get_database()
    query = """
        SELECT c.courseCode, c.course_name, COUNT(e.u_id) as num_students
        FROM Courses c
        JOIN Enrolled e ON c.courseCode = e.courseCode
        GROUP BY c.courseCode
        ORDER BY num_students DESC
        LIMIT 10;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def get_top_10_students_by_average():
    db = get_database()
    query = """
        SELECT s.stud_id, s.fName, s.lName, AVG(g.grade) as average_grade
        FROM Students s
        JOIN Grades g ON s.stud_id = g.s_id
        GROUP BY s.stud_id
        ORDER BY average_grade DESC
        LIMIT 10;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result