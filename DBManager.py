import mysql.connector
import nameGenerator
import datetime as date

def get_database():
    db = mysql.connector.connect(
        user="root",password="UltimaPass420",
        host="localhost",database="eclassroom",
        auth_plugin="mysql_native_password")
    return db

def create_tables():
    db = get_database()
    cursor = db.cursor(dictionary=True)
    with open('Database_Queries.sql', 'r') as sqlFile:
        res = cursor.execute(sqlFile.read(), multi=True)
        for _ in res:
            continue
        
def populate_tables():
    fullNames = nameGenerator.getFullNames()
    genCreateSQL()
    genInsertSQL(fullNames)
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
    db.close()
    
def genCreateSQL():
    file = open('CreateQueries.sql','w')
    
    query = "DROP DATABASE IF EXISTS eclassroom;\n"
    query += "CREATE DATABASE eclassroom;\n"
    query += "USE eclassroom;\n\n"
    file.write(query)
    
    query = "CREATE TABLE Users(\n"
    query += "    userID int PRIMARY KEY,\n"
    query += "    firstName varchar(100),\n"
    query += "    lastName varchar(100),\n"
    query += "    email varchar(100),\n"
    query += "    passW varchar(100));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Employees(\n"
    query += "    userID int PRIMARY KEY,\n"
    query += "    employeeType varchar(8),\n"
    query += "    salary int,\n"
    query += "    FOREIGN KEY (userID) REFERENCES Users (userID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Students(\n"
    query += "    studentID int PRIMARY KEY,\n"
    query += "    level varchar(13),\n"
    query += "    tuition int,\n"
    query += "    FOREIGN KEY studentID REFERENCES Users (userID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Courses(\n"
    query += "    courseCode varchar(50) PRIMARY KEY,\n"
    query += "    courseName varchar(255),\n"
    query += "    faculty varchar(100),\n"
    query += "    credits int);\n\n"
    file.write(query)
    
    query = "CREATE TABLE CourseMembers(\n"
    query += "    userID int NOT NULL,\n"
    query += "    courseCode varchar(50) NOT NULL,\n"
    query += "    CONSTRAINT PK_Members PRIMARY KEY (userID,courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Forums(\n"
    query += "    forumID int PRIMARY KEY,\n"
    query += "    forumTitle varchar(200),\n"
    query += "    forumDetails varchar(200),\n"
    query += "    courseCode varchar(50),\n"
    query += "    dateCreated date,\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Threads(\n"
    query += "    threadID int PRIMARY KEY,\n"
    query += "    userID int,\n"
    query += "    forumID int,\n"
    query += "    threadDetails varchar(255),\n"
    query += "    replyID int,\n"
    query += "    dateCreated date,\n"
    query += "    FOREIGN KEY (userID) REFERENCES Users(userID),\n"
    query += "    FOREIGN KEY (forumID) REFERENCES Forums(forumID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Sections(\n"
    query += "    sectionID int PRIMARY KEY,\n"
    query += "    courseCode varchar(50),\n"
    query += "    sectionName varchar(100),\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Content(\n"
    query += "    contentID int PRIMARY KEY,\n"
    query += "    sectionID int,\n"
    query += "    details varchar(255),\n"
    query += "    fileName varchar(100),\n"
    query += "    FOREIGN KEY (sectionID) REFERENCES Sections(sectionID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Assignments(\n"
    query += "    assignmentID int PRIMARY KEY,\n"
    query += "    dueDate date,\n"
    query += "    FOREIGN KEY (assignmentID) REFERENCES Content(contentID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Submissions(\n"
    query += "    assignmentID int,\n"
    query += "    studentID int,\n"
    query += "    fileName varchar(255),\n"
    query += "    dateSubmitted date,\n"
    query += "    CONSTRAINT PK_Subs PRIMARY KEY (assignmentID,studentID),\n"
    query += "    FOREIGN KEY assignmentID REFERENCES Assignments (assignmentID),\n"
    query += "    FOREIGN KEY studentID REFERENCES Students (studentID));\n\n"
    file.write(query)
    
    query = "CREATE TABLE CalendarEvents(\n"
    query += "    eventID int PRIMARY KEY,\n"
    query += "    eventName varchar(255),\n"
    query += "    eventDetails varchar(255),\n"
    query += "    eventDate date);\n\n"
    file.write(query)
    
    query = "CREATE TABLE AssignmentEvents(\n"
    query += "    eventID int,\n"
    query += "    assignmentID varchar(255),\n"
    query += "    CONSTRAINT PK_AEvents PRIMARY KEY (eventID,assignmentID),\n"
    query += "    FOREIGN KEY eventID REFERENCES CalendarEvents (eventID),\n"
    query += "    FOREIGN KEY assignmentID REFERENCES Assignments (assignmentID));\n\n"
    file.write(query)
    
def genInsertSQL(names):
    sqlFile = open('InsertQueries.sql', 'w')
    sqlFile.write("USE eclassroom;\n\n")
    
    employeeQuery = "INSERT INTO Employees (userID,employeeType,salary) VALUES (1,'ADMIN',100000),(2,'LECTURER',80000);\n\n"        
    studentQuery = "INSERT INTO Students (studentID,level,tuition) VALUES \n"
    userQuery = "INSERT INTO Users (userID,firstName,lastName,email,passW) VALUES \n"
    userQuery += "    (1,'Chukwudi','Ojuro','chukwudiojuro@gmail.com','password'),\n"
    
    
    count = 620000000
    for name in names:
        names = name.split(" ")
        
        studentQuery +=f"    ({count},'UNDERGRAD',45000),\n"
        userQuery += f"    ({count},'{names[0]}','{names[1]}','{names[0]}{names[1]}@gmail.com','{names[1]}{names[0]}'),\n"
        
        count+=1
        
    studentQuery += "    (3,'GRAD',45000);\n\n"
    userQuery += "    (3,'Bob','Turner','bobturner@gmail.com','password'),\n"
    userQuery += "    (2,'Chuck','Falcon','chuckfalcon@gmail.com','password');\n\n"

    sqlFile.write(userQuery)
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
