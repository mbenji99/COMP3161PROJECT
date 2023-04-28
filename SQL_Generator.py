import itertools
import names
import random
import DBManager as dbm

    
def getFirstNames():
    fNames = set()
    while len(fNames) < 317:
        if len(fNames) < 158:
            fNames.add(names.get_first_name(gender="male"))
        else:
            fNames.add(names.get_first_name(gender="female"))

    return list(fNames)

def getLastNames():
    lNames = set()
    while len(lNames) < 316:
        lNames.add(names.get_last_name())

    return list(lNames)


def getFullNames():
    fullNames = []
    fNames = getFirstNames()
    lNames = getLastNames()
    
    fullNames = [f"{fn} {ln}" for fn, ln in itertools.product(fNames, lNames)]
    
    random.shuffle(fullNames)
    return fullNames

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
    query += "    FOREIGN KEY (u_id) REFERENCES Students (stud_id),\n"
    query += "    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode),\n"
    query += "    PRIMARY KEY(u_id,courseCode));\n\n"
    file.write(query)
    
    query = "CREATE TABLE Course_Maintainers(\n"
    query += "    lect_id int NOT NULL,\n"
    query += "    courseCode varchar(50) NOT NULL,\n"
    query += "    FOREIGN KEY (lect_id) REFERENCES Lecturers (lect_id),\n"
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
    query += "    assignment_id int,\n"
    query += "    FOREIGN KEY (event_id) REFERENCES CalendarEvents (event_id),\n"
    query += "    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id));\n\n"
    file.write(query)

def genInsertSQL():
    names = getFullNames()
    sqlFile = open('Queries/InsertQueries.sql', 'w')
    insert_sqlFile = open("Queries/InsertQueries1.sql",'w')
    sqlFile.write("USE eclass;\n\n")
    
    # Inserting values into Courses table
    courseQuery = "INSERT INTO Courses (courseCode,course_name,start_date) VALUES\n"
    courseDomains = ["COMP","ECON","MATH","INFO","PHYS","BIOC","CHEM"]
    courseCodes = []
    
    for _ in range(200):
        courseNumber = random.randint(1000,4000)
        domain = courseDomains[random.randint(0,len(courseDomains)-1)]
        cCode = domain+str(courseNumber)
        
        while  cCode in courseCodes or cCode == "COMP3161":
            courseNumber = random.randint(1000,4000)
            domain = courseDomains[random.randint(0,len(courseDomains)-1)]
            cCode = domain+str(courseNumber)
        
        courseCodes.append(cCode)
        courseQuery += f"    ('{cCode}','Some Course Name','5/Sept'),\n"
    courseQuery += "    ('COMP3161','Database Management Systems','5/Jan');\n\n"
    sqlFile.write(courseQuery)
    sqlFile.close()
    
    count = 620000000
    i_count = 0
    q_count = 1
    mod_amount = 3000
    for n in range(len(names)):
        name = names[n].split(" ")
        numEnrol = random.randint(3,6)
        enrolQuery = "INSERT INTO Enrolled (u_id,courseCode) VALUES "
        
        if n % mod_amount == 0 and n>= mod_amount:
            q_count+=1
            insert_sqlFile.close()
            insert_sqlFile = open(f"Queries/InsertQueries{q_count}.sql",'w')
        
        random.shuffle(courseCodes)
        for i in range(numEnrol):
            if i == (numEnrol-1):
                enrolQuery += f"({count},'{courseCodes[i]}');\n"
            else:
                enrolQuery += f"({count},'{courseCodes[i]}'),"
        
        studentQuery =f"INSERT INTO Students VALUES ({count},'UNDERGRAD','01-01-2020');\n"
        userQuery = f"INSERT INTO Users VALUES ({count},'{name[0]}','{name[1]}','{name[0]}{name[1]}@gmail.com','{name[1]}{name[0]}');\n"
        
        insert_sqlFile.write(userQuery)
        insert_sqlFile.write(studentQuery)
        insert_sqlFile.write(enrolQuery)
        
        count+=1
        i_count+=1
        
    
    query = "INSERT INTO Users VALUES (3,'Bob','Turner','bobturner@gmail.com','password'),\n"
    query += "    (2,'Chuck','Falcon','chuckfalcon@gmail.com','password'),\n"
    query += "    (1,'Chukwudi','Ojuro','chukwudiojuro@gmail.com','password');\n\n"
    insert_sqlFile.write(query)
    
    query = "INSERT INTO Students VALUES (3,'GRAD',45000);\n\n"
    insert_sqlFile.write(query)
    
    query = f"INSERT INTO Courses VALUES (3,'{courseCodes[0]}'),\n    (3,'{courseCodes[1]}'),\n    (3,'{courseCodes[2]}');\n\n"
    insert_sqlFile.write(query)
    
    query = "INSERT INTO Admins (admin_id) VALUES (1);\n\n"        
    insert_sqlFile.write(query)
    
    query = "INSERT INTO Lecturers (lect_id,salary) VALUES (2,80000);\n\n"  
    insert_sqlFile.write(query)
    
    insert_sqlFile.close()

def executeSQL():
    db = dbm.get_database()
    cursor = db.cursor()
    
    with open('CreateQueries.sql', 'r') as sqlFile:
        res = cursor.execute(sqlFile.read(), multi=True)
        for _ in res:
            continue
    
    with open('Queries/InsertQueries.sql', 'r') as sqlFile:
        res = cursor.execute(sqlFile.read(), multi=True)
        for _ in res:
            continue
    
     
    for i in range(1,34):
        print("Executing SQL file "+str(i))
        with open('Queries/InsertQueries'+str(i)+'.sql', 'r') as sqlFile:
            res = cursor.execute(sqlFile.read(), multi=True)
            for _ in res:
                continue
            sqlFile.close()
        print("SQL File "+str(i)+" finished.")
    
    '''with open('Queries/InsertQueries1.sql', 'r') as sqlFile:
        res = cursor.execute(sqlFile.read(), multi=True)
        for _ in res:
            continue'''
    
    db.commit()
    cursor.close()
    cursor.close()
    
genCreateSQL()
genInsertSQL()
executeSQL()