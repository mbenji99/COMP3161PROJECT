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
workbook = openpyxl.load_workbook(r'C:\Users\Suzette Benjamin\Downloads\Comp3161\Final Assignment\last names.xlsx')
worksheet = workbook.active

# Iterate over the rows and get the data from column A
for row in worksheet.iter_rows(min_row=2, min_col=1, max_col=1):
    last_name = row[0].value

    # Insert the data into the MySQL table
    sql = "INSERT INTO lastNames (l_name) VALUES (%s)"
    val = (last_name,)
    cursor.execute(sql, val)

# Commit the changes and close the connection
db.commit()
db.close()
