CREATE DATABASE IF NOT EXISTS School;
USE School;

CREATE TABLE Users(
    u_id int PRIMARY KEY,
    f_name varchar(100),
    l_name varchar(100),
    email varchar(100),
    passW varchar(100));

CREATE TABLE IF NOT EXISTS Student (
    s_id CHAR(9) PRIMARY KEY,
    level varchar(50),
    date_enrolled varchar(20),
    Foreign key (s_id) References Users (u_id),
-- chk_student_courses: ensures that no student is enrolled in more than 6 courses
    CONSTRAINT chk_student_courses CHECK (s_id NOT IN (
        SELECT s_id FROM Enrollments GROUP BY s_id HAVING COUNT(*) > 6
)));

CREATE TABLE IF NOT EXISTS firstNames(f_name VARCHAR(50));
CREATE TABLE IF NOT EXISTS lastNames(l_name VARCHAR(50));
CREATE TABLE IF NOT EXISTS emailDomains(domain VARCHAR(50));

INSERT INTO emailDomains(domain) VALUES ('hotmail.com'),('gmail.com'), ('outlook.com');

SET @i = 1;

DELIMITER $$

CREATE PROCEDURE Generate_Students()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE (i <= 100000) DO
        SET @s_id = CONCAT('621', LPAD(i, 6, '0'));
        SET @s_first = (SELECT f_name FROM firstNames ORDER BY RAND() LIMIT 1);
        SET @s_last = (SELECT l_name FROM lastNames ORDER BY RAND() LIMIT 1);
        SET @s_name = CONCAT(@s_first, ' ', @s_last);
        SET @s_email = CONCAT(@s_first, '.', @s_last, '@', (SELECT domain FROM emailDomains ORDER BY RAND() LIMIT 1));
        INSERT INTO Student (s_id, s_name, s_email) VALUES (@s_id, @s_name, @s_email);
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

CALL Generate_Students();

Create table Courses (
	c_id varchar(50) Primary key, 
	course_name varchar(255), 
    start_date Date, 
-- chk_course_members: ensures that each course has at least 10 members
    CONSTRAINT chk_course_members CHECK (course_id IN (
        SELECT c_id FROM CourseMembers GROUP BY c_id HAVING COUNT(*) >= 10
    ))
);
    
Create table Enrollments ( 
	enrollment_id int Primary key,
	s_id int,
	c_id int,
    date_enrolled DATE,
    Foreign key (s_id) References Student(s_id),
    Foreign key (c_id) References Courses(c_id)
);

	
Create table Course_Maintainers (
	lec_id int(50) Primary key,
    salary int(50),
    Foreign Key (lec_id) References Users(u_id),
-- chk_lecturer_courses: ensures that no lecturer is assigned to teach more than 5 courses
    Constraint chk_lecturer_courses Check (lec_id NOT IN (
        Select lec_id From CourseAssignments GROUP BY lec_id HAVING COUNT(*) > 5
    ))
);

Create Table Admins (
    admin_id int(50) Primary key,
    Foreign Key admin_id References Users (u_id)
)

Create table CourseAssignments (
    course_assignment_id int Primary key,
    c_id int,
    lec_id int,
    date_assigned Date,
    Foreign key (c_id) References Courses(c_id),
    Foreign key (lec_id) References Course_Maintainers(lec_id)
);

Create table CourseMembers (
    course_member_id int Primary key,
    c_id int,
    s_id int,
    lec_id int,
    date_joined Date,
    Foreign key (c_id) References Courses(c_id),
    Foreign key (s_id) References Student(s_id),
    Foreign key (lec_id) References Course_Maintainers(lec_id)
);
-- chk_student_enrollments: ensures that each student is enrolled in at least 3 courses
Alter table Students ADD CONSTRAINT chk_student_enrollments CHECK (s_id IN (
    Select s_id From Enrollments GROUP BY s_id HAVING COUNT(*) >= 3
));

-- chk_lecturer_assignments: ensures that each lecturer is assigned to teach at least 1 course
Alter table Course_Maintainers ADD CONSTRAINT chk_lecturer_assignments CHECK (l_id IN (
    Select lec_id From CourseAssignments GROUP BY lec_id HAVING COUNT(*) >= 1
));

CREATE TABLE Forums(
    forum_id int PRIMARY KEY,
    forum_title varchar(200),
    forum_details varchar(200),
    c_id varchar(50),
    date_created date,
    FOREIGN KEY (c_id) REFERENCES Courses(c_id));

CREATE TABLE Threads(
    thread_id int PRIMARY KEY,
    u_id int,
    forum_id int,
    thread_details varchar(255),
    reply_id int,
    date_created date,
    FOREIGN KEY (u_id) REFERENCES Users(u_id),
    FOREIGN KEY (forum_id) REFERENCES Forums(forum_id));


select * from Course_Maintainers;

