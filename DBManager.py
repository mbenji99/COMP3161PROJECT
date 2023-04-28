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
    
def get_courses(case):
    if case == "All":
        pass
    else:
        pass

def register_for_course(info):
    pass

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
    pass

def get_date_events(date,studentID):
    pass

def create_calendar_event(info):
    pass

def create_forum(info):
    pass

def get_forums(courseCode):
    pass

def create_thread(info):
    pass
