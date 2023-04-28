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

'''
ef create_tables():
    db = get_database()
    cursor = db.cursor(dictionary=True)
    with open('CreateQueries.sql', 'r') as sqlFile:
        res = cursor.execute(sqlFile.read(), multi=True)
        for _ in res:
            continue
        
# needs to be refactored to fit updated database schema
def populate_tables():
    fullNames = nameGenerator.getFullNames()
    genCreateSQL()
    genInsertSQL()
    db = get_database()
    cursor = db.cursor()
    
    count = 620000000
    query = "INSERT INTO Users (userID,firstName,lastName,userType,email,passW) VALUES "
    for name in fullNames:
        names = name.split(" ")
        query += f"({count},'{names[0]}','{names[1]}','STUDENT','{names[0]}{names[1]}@gmail.com','{names[1]}{names[0]}'),"
        count+=1

    query += f"(620,'Chukwudi','Ojuro','ADMIN','chukwudiojuro@gmail.com','password')"

    cursor.execute(query)
    db.commit()
    
    cursor.close()
    db.close()'''


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
    
    if info['userType'] == "STUDENT":
        query = "INSERT INTO Students (s_id,level,date_enrolled) VALUES "
        query += f"({info['userID']},'UNDERGRAD', CURRENT_DATE())"
    elif info['userType'] == "LECTURER":
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
    
    query = f"SELECT * FROM Users WHERE userID={userID} AND passW='{passW}'"
    cursor.execute(query)
    res = cursor.fetchone()
    
    if res is not None:
        return res[0]
    else:
        return "Null"
    
def create_courses(info):
    # Create a new course with the provided information
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Courses (c_id, course_name, start_date) VALUES (%s, %s, %s)",
                   (info['c_id'], info['course_name'], info['start_date']))
    connection.commit()
    
def get_courses(case):
    cursor = connection.cursor(dictionary=True)
    if case == "All":
        cursor.execute("SELECT * FROM Courses")
        return cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Courses WHERE c_id=%s", (case,))
        return cursor.fetchone()

def register_for_course(info):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO CourseMembers (c_id, s_id, lec_id, date_joined) VALUES (%s, %s, %s, %s)",
                   (info['c_id'], info['s_id'], info['lec_id'], info['date_joined']))
    connection.commit()

def assign_lecturer(courseCode,lecturerID):
    pass

def get_members(course):
    db = get_database()
    cursor = db.cursor()
    
    c_query = f"SELECT * FROM Courses WHERE courseCode = '{course}'"
    cursor.execute(c_query)
    res = cursor.fetchone()
    
    if res is None:
        return None
    
    stud_query = f"SELECT * FROM Enrolled WHERE courseCode = '{course}'"
    cursor.execute(stud_query)
    students = cursor.fetchall()
    
    lect_query = f"SELECT * FROM Course_Maintainers WHERE courseCode = '{course}'"
    cursor.execute(lect_query)
    lecturers = cursor.fetchall()
    
    cursor.close()
    db.close()
    return [lecturers,students]
    

def get_course_events(courseCode):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CourseAssignments WHERE c_id=%s", (courseCode,))
    return cursor.fetchall()

def get_date_events(date, studentID):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CourseAssignments WHERE date_assigned=%s AND c_id IN \
                    (SELECT c_id FROM CourseMembers WHERE s_id=%s)", (date, studentID))
    return cursor.fetchall()

def create_calendar_event(info):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO CourseAssignments (course_assignment_id, c_id, lec_id, date_assigned) \
                    VALUES (%s, %s, %s, %s)", (info['course_assignment_id'], info['c_id'], info['lec_id'], info['date_assigned']))
    connection.commit()

def create_forum(info):
    pass

def get_forums(courseCode):
    pass

def create_thread(info):
    pass

def get_courses_with_50_or_more_students():
    query = """
        SELECT c.c_id, c.course_name, COUNT(cm.course_member_id) as num_students
        FROM Courses c
        JOIN CourseMembers cm ON c.c_id = cm.c_id
        GROUP BY c.c_id
        HAVING COUNT(cm.course_member_id) >= 50
        ORDER BY num_students DESC;
    """
    result = db.session.execute(query).fetchall()
    return [dict(row) for row in result]

def get_students_with_5_or_more_courses():
    query = """
        SELECT s.s_id, s.first_name, s.last_name, COUNT(cm.course_member_id) as num_courses
        FROM Student s
        JOIN CourseMembers cm ON s.s_id = cm.s_id
        GROUP BY s.s_id
        HAVING COUNT(cm.course_member_id) >= 5
        ORDER BY num_courses DESC;
    """
    result = db.session.execute(query).fetchall()
    return [dict(row) for row in result]

def get_lecturers_with_3_or_more_courses():
    query = """
        SELECT cm.lec_id, cm.first_name, cm.last_name, COUNT(ca.course_assignment_id) as num_courses
        FROM CourseAssignments ca
        JOIN Course_Maintainers cm ON ca.lec_id = cm.lec_id
        GROUP BY cm.lec_id
        HAVING COUNT(ca.course_assignment_id) >= 3
        ORDER BY num_courses DESC;
    """
    result = db.session.execute(query).fetchall()
    return [dict(row) for row in result]

def get_top_10_enrolled_courses():
    query = """
        SELECT c.course_name, COUNT(cm.course_member_id) as num_students
        FROM Courses c
        JOIN CourseMembers cm ON c.c_id = cm.c_id
        GROUP BY c.c_id
        ORDER BY num_students DESC
        LIMIT 10;
    """
    result = db.session.execute(query).fetchall()
    return [dict(row) for row in result]

def get_top_10_students_by_average():
    query = """
        SELECT s.s_id, s.first_name, s.last_name, AVG(g.grade) as average_grade
        FROM Student s
        JOIN Grades g ON s.s_id = g.s_id
        GROUP BY s.s_id
        ORDER BY average_grade DESC
        LIMIT 10;
    """
    result = db.session.execute(query).fetchall()
    return [dict(row) for row in result]
