DROP DATABASE IF EXISTS eclass;
CREATE DATABASE IF NOT EXISTS eclass;
USE eclass;

CREATE TABLE Users(
    u_id int PRIMARY KEY,
    fName varchar(100),
    lName varchar(100),
    email varchar(100),
    passW varchar(100));

CREATE TABLE Admins(
    admin_id int PRIMARY KEY,
    FOREIGN KEY (admin_id) REFERENCES Users (u_id));

CREATE TABLE Lecturers(
    lect_id int PRIMARY KEY,
    salary int,
    FOREIGN KEY (lect_id) REFERENCES Users (u_id));

CREATE TABLE Students(
    stud_id int PRIMARY KEY,
    level varchar(13),
    date_enrolled varchar(20),
    FOREIGN KEY (stud_id) REFERENCES Users (u_id));

CREATE TABLE Courses(
    courseCode varchar(50) PRIMARY KEY,
    course_name varchar(255),
    start_date varchar(20),
    credits int);

CREATE TABLE Enrolled(
    u_id int NOT NULL,
    courseCode varchar(50) NOT NULL,
    FOREIGN KEY (u_id) REFERENCES Students (stud_id),
    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode),
    PRIMARY KEY(u_id,courseCode));

CREATE TABLE Course_Maintainers(
    lect_id int NOT NULL,
    courseCode varchar(50) NOT NULL,
    FOREIGN KEY (lect_id) REFERENCES Lecturers (lect_id),
    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode),
    CONSTRAINT PK_Members PRIMARY KEY (lect_id,courseCode));

CREATE TABLE Forums(
    forum_id int PRIMARY KEY AUTO_INCREMENT,
    forum_title varchar(200),
    forum_details varchar(200),
    courseCode varchar(50),
    date_created date,
    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));

CREATE TABLE Threads(
    thread_id int PRIMARY KEY AUTO_INCREMENT,
    u_id int,
    forum_id int,
    thread_details varchar(255),
    reply_id int,
    date_created date,
    FOREIGN KEY (u_id) REFERENCES Users(u_id),
    FOREIGN KEY (forum_id) REFERENCES Forums(forum_id));

CREATE TABLE Sections(
    section_id int PRIMARY KEY AUTO_INCREMENT,
    courseCode varchar(50),
    section_name varchar(100),
    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));

CREATE TABLE Content(
    content_id int PRIMARY KEY AUTO_INCREMENT,
    section_id int,
    details varchar(255),
    file_name varchar(100),
    FOREIGN KEY (section_id) REFERENCES Sections(section_id));

CREATE TABLE Assignments(
    assignment_id int PRIMARY KEY,
    due_date date,
    FOREIGN KEY (assignment_id) REFERENCES Content(content_id));

CREATE TABLE Submissions(
    assignment_id int,
    stud_id int,
    file_name varchar(255),
    date_submitted date,
    PRIMARY KEY (assignment_id,stud_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id),
    FOREIGN KEY (stud_id) REFERENCES Students (stud_id));

CREATE TABLE CalendarEvents(
    event_id int PRIMARY KEY AUTO_INCREMENT,
    courseCode varchar(255),
    event_name varchar(255),
    event_details varchar(255),
    event_date varchar(20),
    FOREIGN KEY (courseCode) REFERENCES Courses (courseCode));

CREATE TABLE AssignmentEvents(
    event_id int PRIMARY KEY,
    assignment_id int,
    FOREIGN KEY (event_id) REFERENCES CalendarEvents (event_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id));

