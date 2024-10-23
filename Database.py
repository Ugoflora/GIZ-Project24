import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS students (id integer PRIMARY KEY, first_name Text, last_name Text, email Text, phone_number Text, course Text, bank_name Text, account_number integer, gender Text, reg_date Text)"

ADD_STUDENT = "INSERT INTO students(first_name, last_name, email, phone_number, course,  bank_name, account_number, gender, reg_date) VALUES (?,?,?,?,?,?,?,?,?)"

VIEW_STUDENTS = "SELECT * FROM STUDENTS"

VIEW_STUDENT_BY_NAME = "SELECT * FROM students WHERE first_name = ?"

VIEW_STUDENTS_WITHIN_A_CLASS = "SELECT * FROM students WHERE course = ?"

DELETE_STUDENT = "DELETE FROM students WHERE id = ?"


def createConnectDatabase():
    """Creates a database and connects to it"""
    return sqlite3.connect("Reg.db")


def createTable(connection):
    """Creates a table in the database"""
    with connection:
        connection.execute(CREATE_TABLE)

def addStudent(connection, fname, lname, email, phone_number, course, bank_name,account_number, gender, reg_date):
    with connection:
        connection.execute(ADD_STUDENT, (fname, lname, email, phone_number, course, bank_name,account_number, gender, reg_date))
        
def viewStudents(connection):
    with connection:
        students = connection.execute(VIEW_STUDENTS).fetchall()
        return students
    
def viewStudentByName(connection, name):
    with connection:
        return connection.execute(VIEW_STUDENT_BY_NAME, (name,)).fetchall()
    
def viewStudentsWithinAClass(connection, course):
    with connection:
        return connection.execute(VIEW_STUDENTS_WITHIN_A_CLASS, (course,)).fetchall()
    
def deleteStudent(connection, id):
    with connection:
        return connection.execute(DELETE_STUDENT, id)
    
def editDetail(connection, data, replacement, id):
    EDIT = f"""
    UPDATE students
    SET {data} = ?
    WHERE id = ?;
    """
    with connection:
        return connection.execute(EDIT, (replacement, id))