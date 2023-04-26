DROP DATABASE IF EXISTS eclassroom;
CREATE DATABASE eclassroom;
USE eclassroom;

CREATE TABLE Users(
    userID int PRIMARY KEY,
    firstName varchar(100),
    lastName varchar(100),
    email varchar(100),
    passW varchar(100));

CREATE TABLE Employees(
    userID int PRIMARY KEY,
    employeeType varchar(8),
    salary int,
    FOREIGN KEY (userID) REFERENCES Users (userID));

CREATE TABLE Students(
    studentID int PRIMARY KEY,
    level varchar(13),
    tuition int,
    FOREIGN KEY studentID REFERENCES Users (userID));

CREATE TABLE Courses(
    courseCode varchar(50) PRIMARY KEY,
    courseName varchar(255),
    faculty varchar(100),
    credits int);

CREATE TABLE CourseMembers(
    userID int NOT NULL,
    courseCode varchar(50) NOT NULL,
    CONSTRAINT PK_Members PRIMARY KEY (userID,courseCode));

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

CREATE TABLE Sections(
    sectionID int PRIMARY KEY,
    courseCode varchar(50),
    sectionName varchar(100),
    FOREIGN KEY (courseCode) REFERENCES Courses(courseCode));

CREATE TABLE Content(
    contentID int PRIMARY KEY,
    sectionID int,
    details varchar(255),
    fileName varchar(100),
    FOREIGN KEY (sectionID) REFERENCES Sections(sectionID));

CREATE TABLE Assignments(
    assignmentID int PRIMARY KEY,
    dueDate date,
    FOREIGN KEY (assignmentID) REFERENCES Content(contentID));

CREATE TABLE Submissions(
    assignmentID int,
    studentID int,
    fileName varchar(255),
    dateSubmitted date,
    CONSTRAINT PK_Subs PRIMARY KEY (assignmentID,studentID),
    FOREIGN KEY assignmentID REFERENCES Assignments (assignmentID),
    FOREIGN KEY studentID REFERENCES Students (studentID));

CREATE TABLE CalendarEvents(
    eventID int PRIMARY KEY,
    eventName varchar(255),
    eventDetails varchar(255),
    eventDate date);

CREATE TABLE AssignmentEvents(
    eventID int,
    assignmentID varchar(255),
    CONSTRAINT PK_AEvents PRIMARY KEY (eventID,assignmentID),
    FOREIGN KEY eventID REFERENCES CalendarEvents (eventID),
    FOREIGN KEY assignmentID REFERENCES Assignments (assignmentID));

