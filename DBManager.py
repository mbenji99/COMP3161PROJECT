import mysql.connector

USER,PASS = "root","UltimaPass420"
HOST,DB = "localhost","eclass"
AUTH = "mysql_native_password"

def get_database():
    db = mysql.connector.connect(
        user=USER,password=PASS,
        host=HOST,database=DB,
        auth_plugin=AUTH)
    return db

def register_user(info):
    db = get_database()
    cursor = db.cursor()
    
    userID,passW,userType = info['userID'],info['passW'],info['userType']
    fName,lName = info['fName'],info['lName']
    
    # Check if userID already exists
    query = f"SELECT * FROM Users WHERE u_id = '{userID}'"
    cursor.execute(query)
    res = cursor.fetchone()
    
    if res is not None:
        return 0
    
    # If unused, insert into table
    query = f"INSERT INTO Users (u_id, f_name, l_name, email, passW) VALUES "
    query += f"({userID},{fName},{lName},{fName}{lName}@gmail.com,{passW})"
    
    if userType == "STUDENT":
        query = "INSERT INTO Students (s_id,level,date_enrolled) VALUES "
        query += f"({info['userID']},'UNDERGRAD', CURRENT_DATE())"
    elif userType == "LECTURER":
        query = "INSERT INTO Course_Maintainers (lec_id,salary) VALUES "
        query += f"({info['userID']},80000)"
    cursor.execute(query)
    
    db.commit()
    
    cursor.close()
    db.close()
    return 1

def login_user(userID, passW):
    db = get_database()
    cursor = db.cursor()
    
    query = f"SELECT * FROM Users WHERE u_id = {userID} AND passW = '{passW}'"
    cursor.execute(query)
    res = cursor.fetchone()
    
    if res is not None:
        res = getUserType(userID)
    
    return res

def getUserType(id):
    db = get_database()
    cursor = db.cursor()
    
    query = f"SELECT * FROM Admins WHERE admin_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        return "ADMIN"
    
    query = f"SELECT * FROM Students WHERE stud_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        return "STUDENT"
    
    query = f"SELECT * FROM Teachers WHERE lect_id = {id}"
    cursor.execute(query)
    res = cursor.fetchone()
    if res is not None:
        return "LECTURER"


def get_courses(case):
    db = get_database()
    cursor = db.cursor()
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
    cursor = db.cursor()
    
    userType = getUserType(id)
    query = ""
    
    if userType == "LECTURER":
        query = f"SELECT courseCodes FROM Course_Maintainers WHERE lect_id = {id}"
    elif userType == "STUDENT":
        query = f"SELECT courseCodes FROM Enrolled WHERE u_id = {id}"
    else:
        return
    
    cursor.execute(query)
    res = cursor.fetchall()
    
    cursor.close()
    db.close()
    return res
    
def create_course(info):
    # Create a new course with the provided information
    db = get_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Courses (courseCode, course_name, start_date, credits) VALUES (%s, %s, %s, %s)",
                   (info['courseCode'], info['course_name'], info['start_date'], info['credits']))
    db.commit()
    
    cursor.close()
    db.close()

def register_for_course(info):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Enrolled (u_id, courseCode) VALUES (%s, %s)",
                   (info['stud_id'], info['courseCode']))
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
    cursor.execute("SELECT * FROM Courses WHERE start_date=%s AND courseCode IN \
                    (SELECT courseCode FROM Enrolled WHERE u_id=%s)", (date, student_id))
    res = cursor.fetchall()

    cursor.close()
    db.close()
    return res

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
    
    cursor.execute("INSERT INTO CalendarEvents (event_name, courseCode, event_details, event_date) \
                    VALUES (%s, %s, %s, %s)", (info['event_name'], info['courseCode'], info['event_details'], info['event_date']))
    
    cursor.execute("INSERT INTO AssignmentEvents (event_id, assignment_id) \
                    VALUES (%s, %s)", (info['event_id'], info['assignment_id']))
    db.commit()

    cursor.close()
    db.close()

def assign_lecturer(courseCode,lecturerID):
    pass

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
    lecturer = cursor.fetchall()
    
    cursor.close()
    db.close()
    return [lecturer,students]
    

def create_forum(info):
    pass

def get_forums(courseCode):
    pass

def create_thread(info):
    pass

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
    return result

def get_lecturers_with_3_or_more_courses():
    db = get_database()
    query = """
        SELECT Students.stud_id, Users.fName, Users.lName, COUNT(Enrolled.courseCode) as num_courses
        FROM Students
        JOIN Enrolled ON Students.stud_id = Enrolled.u_id
        JOIN Users ON Students.stud_id = Users.u_id
        GROUP BY Students.stud_id
        HAVING COUNT(Enrolled.courseCode) >= 3
        ORDER BY num_courses DESC;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_top_10_enrolled_courses():
    db = get_database()
    query = """
        SELECT c.course_name, COUNT(e.u_id) as num_students
        FROM Courses c
        JOIN Enrolled e ON c.courseCode = e.courseCode
        GROUP BY c.courseCode
        ORDER BY num_students DESC
        LIMIT 10;
    """
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
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
    return result