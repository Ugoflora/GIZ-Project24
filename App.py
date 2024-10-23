import Database
from datetime import datetime  # Import datetime for automatic registration date

MENU_PROMPT = """ ___ GIZ Program 2024 ___
please choose one of these options

1. Add a new student
2. see all students
3. Find a student by name
4. See number of students per class
5. delete a student
6. edit student details
7.exit

Your Selection:"""

connection = Database.createConnectDatabase()
Database.createTable(connection)

#using python walrus operator
while (user_input := input(MENU_PROMPT)) != "7":
    if user_input == "1":
        fname = input("Enter first name: ").capitalize()
        lname = input("Enter last name: ").capitalize()
        email = input('Enter email: ').lower()
        phone_number = input("Enter phone number: ")
        course = input("Enter course: ").capitalize()
        bank_name = input("Enter bank name: ").capitalize()
        account_number = int(input("Enter your account number: "))
        gender = input("Enter gender, M or F:").capitalize()
        reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Automatically generate the registration date
        Database.addStudent(connection, fname, lname, email, phone_number, course, bank_name,account_number, gender, reg_date)
        print(f"{fname} {lname} registered successfully!")
        
    elif user_input == "2":
        students = Database.viewStudents(connection)
        print("\n")
        for student in students:
            print(f"{student[0]} | {student[1]} |{student[2]} |{student[3]} |{student[4]} | {student[5]} |{student[6]} |{student[7]} |{student[8]} |{student[9]} \n ")
        
    elif user_input =="3":
        name = input("Enter student first name: ")
        students = Database.viewStudentByName(connection, name)
        for student in students:
            print(f"{student[0]} | {student[1]} |{student[2]} |{student[3]} |{student[4]} | {student[5]} |{student[6]} |{student[7]} |{student[8]} |{student[9]} \n ")
            
    elif user_input == "4":
        course = input("Enter course name: ")
        students = Database.viewStudentsWithinAClass(connection, course)
        for student in students:
            print(f"{student[0]} | {student[1]} |{student[2]} |{student[3]} |{student[4]} | {student[5]} |{student[6]} |{student[7]} |{student[8]} |{student[9]} \n ")
            
    
    elif user_input == "5":
        id = input("Enter the ID of the student you want to delete: ").lower()
        confirmation = input("Are you sure? ")
        if confirmation == 'yes':
            Database.deleteStudent(connection, id)
            print("successfully deleted!")
        else:
            pass
        
    elif user_input == "6":
        edit = input("what do you want to edit? ").lower()
        student_id = int(input("Enter the student id: "))
        replacement = input("Replace with what? ")
        a,b = edit.split(" ")
        data = a + "_" + b
        Database.editDetail(connection, data, replacement, student_id)
        print(f"{data} updated!")
        
    else:
        print("Input Error!")