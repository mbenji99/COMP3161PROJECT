import mysql.connector
import nameGenerator

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

def genCreateSQL():
    file = open('CreateQueries.sql','w')
    
    query = "DROP DATABASE IF EXISTS eclass;\n"
    query += "CREATE DATABASE IF NOT EXISTS eclass;\n"
    query += "USE eclass;\n\n"
    file.write(query)
    
    query = "CREATE TABLE Users(\n"
    query += "    u_id int PRIMARY KEY,\n"
    query += "    fName varchar(100),\n"
    query += "    lName varchar(100),\n"
    query += "    email varchar(100),\n"
    query += "    passW varchar(100));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Admins(\n"
    query += "    admin_id int PRIMARY KEY,\n"
    query += "    FOREIGN KEY (admin_id) REFERENCES Users (u_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Lecturers(\n"
    query += "    lect_id int PRIMARY KEY,\n"
    query += "    salary int,\n"
    query += "    FOREIGN KEY (lect_id) REFERENCES Users (u_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Students(\n"
    query += "    stud_id int PRIMARY KEY,\n"
    query += "    level varchar(13),\n"
    query += "    date_enrolled varchar(20),\n"
    query += "    FOREIGN KEY (stud_id) REFERENCES Users (u_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Courses(\n"
    query += "    courseCode varchar(50) PRIMARY KEY,\n"
    query += "    course_name varchar(255),\n"
    query += "    start_date varchar(20),\n"
    query += "    credits int);\n\n"
    file.write(query)
    
    query = "CREATE TABLE Enrolled(\n"
    query += "    u_id int NOT NULL,\n"
    query += "    courseCode varchar(50) NOT NULL,\n"
    query += "    FOREIGN KEY (u_id) REFERENCES Students (u_id),\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode),\n"
    query += "    CONSTRAINT PK_Members PRIMARY KEY (u_id,courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Course_Maintainers(\n"
    query += "    lect_id int NOT NULL,\n"
    query += "    courseCode varchar(50) NOT NULL,\n"
    query += "    FOREIGN KEY (lect_id) REFERENCES Lecturers (u_id),\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode),\n"
    query += "    CONSTRAINT PK_Members PRIMARY KEY (lect_id,courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Forums(\n"
    query += "    forum_id int PRIMARY KEY,\n"
    query += "    forum_title varchar(200),\n"
    query += "    forum_details varchar(200),\n"
    query += "    courseCode varchar(50),\n"
    query += "    date_created date,\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Threads(\n"
    query += "    thread_id int PRIMARY KEY,\n"
    query += "    u_id int,\n"
    query += "    forum_id int,\n"
    query += "    thread_details varchar(255),\n"
    query += "    reply_id int,\n"
    query += "    date_created date,\n"
    query += "    FOREIGN KEY (u_id) REFERENCES Users(u_id),\n"
    query += "    FOREIGN KEY (forum_id) REFERENCES Forums(forum_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Sections(\n"
    query += "    section_id int PRIMARY KEY,\n"
    query += "    courseCode varchar(50),\n"
    query += "    section_name varchar(100),\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Content(\n"
    query += "    content_id int PRIMARY KEY,\n"
    query += "    section_id int,\n"
    query += "    details varchar(255),\n"
    query += "    file_name varchar(100),\n"
    query += "    FOREIGN KEY (section_id) REFERENCES Sections(section_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Assignments(\n"
    query += "    assignment_id int PRIMARY KEY,\n"
    query += "    due_date date,\n"
    query += "    FOREIGN KEY (assignment_id) REFERENCES Content(content_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Submissions(\n"
    query += "    assignment_id int,\n"
    query += "    stud_id int,\n"
    query += "    file_name varchar(255),\n"
    query += "    date_submitted date,\n"
    query += "    CONSTRAINT PK_Subs PRIMARY KEY (assignment_id,stud_id),\n"
    query += "    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id),\n"
    query += "    FOREIGN KEY (stud_id) REFERENCES Students (stud_id));\n\n"
    file.write(query)
    
    query = "CREATE TABLE CalendarEvents(\n"
    query += "    event_id int PRIMARY KEY,\n"
    query += "    event_name varchar(255),\n"
    query += "    event_details varchar(255),\n"
    query += "    event_date varchar(20));\n\n"
    file.write(query)
    
    query = "CREATE TABLE AssignmentEvents(\n"
    query += "    event_id int PRIMARY KEY,\n"
    query += "    assignment_id varchar(255),\n"
    query += "    FOREIGN KEY (event_id) REFERENCES CalendarEvents (event_id),\n"
    query += "    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id));\n\n"
    file.write(query)
    
def genInsertSQL():
    names = nameGenerator.getFullNames()
    sqlFile = open('InsertQueries.sql', 'w')
    sqlFile.write("USE eclass;\n\n")
    
    adminQuery = "INSERT INTO Admins (userID) VALUES (1);\n\n"        
    employeeQuery = "INSERT INTO Employees (userID,salary) VALUES (2,80000);\n\n"        
    studentQuery = "INSERT INTO Students (studentID,level,date_enrolled) VALUES \n"
    userQuery = "INSERT INTO Users (userID,firstName,lastName,email,passW) VALUES \n"
    userQuery += "    (1,'Chukwudi','Ojuro','chukwudiojuro@gmail.com','password'),\n"
    
    
    count = 620000000
    for name in names:
        names = name.split(" ")
        
        studentQuery +=f"    ({count},'UNDERGRAD','01-01-2020'),\n"
        userQuery += f"    ({count},'{names[0]}','{names[1]}','{names[0]}{names[1]}@gmail.com','{names[1]}{names[0]}'),\n"
        
        count+=1
        
    studentQuery += "    (3,'GRAD',45000);\n\n"
    userQuery += "    (3,'Bob','Turner','bobturner@gmail.com','password'),\n"
    userQuery += "    (2,'Chuck','Falcon','chuckfalcon@gmail.com','password');\n\n"

    sqlFile.write(userQuery)
    sqlFile.write(adminQuery)
    sqlFile.write(employeeQuery)
    sqlFile.write(studentQuery)
    
    sqlFile.close()

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

def create_courses():
    
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
    pass

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
