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
workbook = openpyxl.load_workbook(r'C:\Users\Suzette Benjamin\Downloads\Comp3161\Final Assignment\Course Maintainers.xlsx', data_only=True)
worksheet = workbook.active

# Iterate over the rows and get the data
for row in worksheet.iter_rows(min_row=2, values_only=True):
    lec_id = row[0]
    lec_name = row[1]
    lec_email = row[2]

    # Insert the data into the MySQL table
    sql = "INSERT INTO Course_Maintainers (lec_id, lec_name, lec_email) VALUES (%s, %s, %s)"
    val = (lec_id, lec_name, lec_email)
    cursor.execute(sql, val)

# Commit the changes and close the connection
db.commit()
db.close()
