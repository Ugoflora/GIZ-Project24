import streamlit as st
import Database  # Assuming Database.py exists in your project directory
from datetime import datetime
import re  # For email validation
from PIL import Image  # Importing PIL to handle images

# Set up the database connection
connection = Database.createConnectDatabase()
Database.createTable(connection)

# Admin credentials (for simplicity, hardcoded)
ADMIN_USERNAME = "Rep2"
ADMIN_PASSWORD = "python2024"

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) in [10, 11]

def validate_account_number(account_number):
    return account_number.isdigit() and len(account_number) == 10

# Admin login function
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Enter Admin Username")
    password = st.text_input("Enter Admin Password", type="password")
    
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials! Please try again.")

# Student registration function
def register_student():
    st.header("Trainee Registration Form")

    fname = st.text_input("First Name").capitalize()
    lname = st.text_input("Last Name").capitalize()
    email = st.text_input('Email').lower()
    phone_number = st.text_input("Phone Number")
    course = st.text_input("Course").capitalize()
    bank_name = st.text_input("Bank Name").capitalize()
    account_number = st.text_input("Account Number")
    gender = st.selectbox("Gender", ["M", "F"])
    reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Register"):
        if not fname or not lname or not email or not phone_number or not course or not bank_name or not account_number or not gender:
            st.error("All fields must be filled!")
        elif not validate_email(email):
            st.error("Invalid email format!")
        elif not validate_phone(phone_number):
            st.error("Phone number must be 10 or 11 digits.")
        elif not validate_account_number(account_number):
            st.error("Account number must be exactly 10 digits.")
        else:
            Database.addStudent(connection, fname, lname, email, phone_number, course, bank_name, account_number, gender, reg_date)
            st.success(f"{fname} {lname} Registered Successfully!")


# Admin-specific functions
def view_students():
    st.header("View All Students")
    students = Database.viewStudents(connection)
    
    if students:
        for student in students:
            st.write(f"{student[0]} | {student[1]} {student[2]} | {student[3]} | {student[4]} | {student[5]} | {student[6]} | {student[7]} | {student[8]} | {student[9]}")
    else:
        st.write("No students registered yet.")

def search_student_by_name():
    st.header("Search Student by Name")
    name = st.text_input("Enter Student First Name")
    
    if st.button("Search"):
        if not name:
            st.error("Please enter a name to search.")
        else:
            students = Database.viewStudentByName(connection, name)
            if students:
                for student in students:
                    st.write(f"{student[0]} | {student[1]} {student[2]} | {student[3]} | {student[4]} | {student[5]} | {student[6]} | {student[7]} | {student[8]} | {student[9]}")
            else:
                st.write("No student found with this name.")

def delete_student():
    st.header("Delete a Student")
    student_id = st.text_input("Enter the ID of the student you want to delete")
    
    if st.button("Delete"):
        if not student_id.isdigit():
            st.error("Please enter a valid numeric student ID.")
        else:
            confirmation = st.checkbox("Are you sure?")
            if confirmation:
                Database.deleteStudent(connection, student_id)
                st.success(f"Student ID {student_id} successfully deleted!")
            else:
                st.warning("Deletion cancelled.")

def edit_student_details():
    st.header("Edit Student Details")
    student_id = st.text_input("Enter the Student ID to edit")
    column_to_edit = st.selectbox("What would you like to edit?", ["First Name", "Last Name", "Email", "Phone Number", "Course", "Bank Name", "Account Number", "Gender"])
    new_value = st.text_input(f"Enter new {column_to_edit}")

    if st.button("Update"):
        if not student_id.isdigit():
            st.error("Please enter a valid numeric student ID.")
        elif not new_value:
            st.error(f"Please enter a new value for {column_to_edit}.")
        else:
            column_map = {
                "First Name": "first_name",
                "Last Name": "last_name",
                "Email": "email",
                "Phone Number": "phone_number",
                "Course": "course",
                "Bank Name": "bank_name",
                "Account Number": "account_number",
                "Gender": "gender"
            }
            Database.editDetail(connection, column_map[column_to_edit], new_value, student_id)
            st.success(f"{column_to_edit} updated successfully!")

# Main function to handle the navigation
def main():
    # Sidebar background color and footer
    st.markdown(
        """
        <style>
        body {
            background-color: #FF0000; /* Red background for main content */
            margin: 0;
            height: 100vh; /* Ensure full height */
            display: flex;
            flex-direction: column;
        }
        .header {
            background-color: #FF0000; /* Red header */
            padding: 20px;
            text-align: center;
            font-size: 24px;
            color: white; /* White text for header */
        }
        .footer {
            background-color: #FF0000; /* Red footer */
            text-align: center;
            font-size: 14px;
            padding: 10px;
            position: relative;
            bottom: 0;
            width: 100%;
            color: white; /* White text for footer */
        }
        .sidebar {
            background-color: #FF0000; /* Red sidebar */
            color: white; /* White text for sidebar */
            height: 100vh; /* Full height */
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* Space between items */
        }
        .content {
            background-color: rgba(255, 255, 255, 0.9); /* Abstract white background for content */
            padding: 20px;
            flex: 1; /* Allow content to take available space */
            box-sizing: border-box;
        }
        .sidebar-footer {
            background-color: #FF0000; /* Red sidebar footer */
            text-align: center;
            font-size: 14px;
            padding: 10px;
            color: white; /* White text for sidebar footer */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom header
    st.markdown('<div class="header">Trainee Registration Portal</div>', unsafe_allow_html=True)

    # Admin login check
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Sidebar for navigation
    menu = st.sidebar.selectbox("Click the dropdown to register", ["Trainee Registration", "Admin Login"])

     # Add video in the sidebar and loop it
    video_file = open("TechWorld3.mp4", "rb")
    st.sidebar.video(video_file, start_time=0)  # Replay from the start automatically

    if menu == "Trainee Registration":
        try:
            student_image = Image.open("giz.png")
            st.image(student_image, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading student image: {e}")
        
        st.markdown('<div class="content">', unsafe_allow_html=True)
        register_student()
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "Admin Login":
        if not st.session_state.logged_in:
            try:
                admin_image = Image.open("giz admin.png")
                st.image(admin_image, use_column_width=True)
            except Exception as e:
                st.error(f"Error loading admin image: {e}")
            
            st.markdown('<div class="content">', unsafe_allow_html=True)
            admin_login()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar footer
    st.sidebar.markdown('<div class="sidebar-footer"> Advanced Python Class 2024 Project </div>', unsafe_allow_html=True)

    # Custom footer for main content
    st.markdown('<div class="footer">GIZ Trainee Portal © 2024</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
