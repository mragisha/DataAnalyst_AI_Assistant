import sqlite3
import pandas as pd

#Load csv data
csv_file = "student_data.csv"
df = pd.read_csv(csv_file)

#create database
connection = sqlite3.connect("student.db")

#Create curson
cursor = connection.cursor()

#Create table
create_table_qurey = """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    COURSE  VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
    );
    """

cursor.execute(create_table_qurey)

# #Insert data
# insert_data_query = """
# INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS)
# VALUES
# ('John Doe', 'Computer Science', 'A', 85),
# ('Jane Smith', 'Mathematics', 'B', 90),
# ('Alice Johnson', 'Physics', 'A', 78),
# ('Bob Brown', 'Chemistry', 'C', 88);
# """

# Insert data into table

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS)
        VALUES (?, ?, ?, ?)""",
        (row['NAME'], row['COURSE'], row['SECTION'], row['MARKS'])
    )

        
    

#cursor.execute(insert_data_query)
#Commit the changes
connection.commit()

data = cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)

#Close the connection
if connection:
    connection.close()
    print("Connection closed")