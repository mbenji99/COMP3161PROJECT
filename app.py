from flask import Flask,make_response,request
import DBManager as dbm

app = Flask(__name__)

@app.route('/')
def index():
    return make_response({"Course":"COMP3161 - Intro to Database Management Systems"},200)

@app.route('/register',methods=['GET','POST'])
def register():
    userID = request.form.get('userID')
    passW = request.form.get('passW')
    fName= request.form.get('fName')
    lName= request.form.get('lName')
    userType = request.form.get('userType')
    userID = str(userID)
    
    if userID[:3] == "620" and len(userID) <= 9:
        dbm.register_user({"userID":userID,"passW":passW,"userType":userType,"fName":fName,"lName":lName})
        return make_response({"Status":"Success"},200)
    else:
        return make_response({"Status": "Invalid user id."},404)

  
@app.route('/users',methods=['GET'])
def getUsers():
    db = dbm.get_database()
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    
    users = []
    
    for uid,fn,ln,email,passw in cursor:
        user = {}
        user['UserID'] = uid
        user['FirstName'] = fn
        user['LastName'] = ln
        user['Email'] = email
        user['Password'] = passw
        users.append(user)
        
        
    cursor.close()
    db.close()
    return make_response(users,200)

if __name__ == "__main__":
    dbm.create_tables()
    dbm.populate_tables()
    #app.run()
    

'''
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
    replyID int,,
    dateCreated date,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (forumID) REFERENCES Forums(forumID));
'''