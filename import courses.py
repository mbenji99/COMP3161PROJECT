import openpyxl
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monday#123",
    database="School"
)
cursor = db.cursor()

# Open the xlsx file and get the worksheet
workbook = openpyxl.load_workbook(r'C:\Users\Suzette Benjamin\Downloads\Comp3161\Final Assignment\Courses1.xlsx')
worksheet = workbook.active

# Iterate over the rows and get the data from columns A and B
for row in worksheet.iter_rows(min_row=2, min_col=1, max_col=2):
    c_id = row[0].value
    course_name = row[1].value

    # Insert the data into the MySQL table
    sql = "INSERT INTO Courses (c_id, course_name) VALUES (%s, %s)"
    val = (c_id, course_name)
    cursor.execute(sql, val)

# Commit the changes and close the connection
db.commit()
db.close()

