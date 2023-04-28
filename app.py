from flask import Flask,make_response,request,session
import DBManager as dbm

session['userType'] = 'VISITOR'
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

@app.route('/Forums/<course>',methods=['GET'])
def getForums(course):
    forums = dbm.get_forums(course)
    return make_response(forums)

@app.route('/CourseMembers/<course>',methods=['GET'])
def getCourseMembers(courseCode):
    members = dbm.get_members(courseCode)
    
    if members is None:
        return make_response("That course does not exist",404)
    
    return make_response(members,200)

if __name__ == "__main__": 
    app.run()
    #dbm.genCreateSQL()
    #dbm.genInsertSQL()