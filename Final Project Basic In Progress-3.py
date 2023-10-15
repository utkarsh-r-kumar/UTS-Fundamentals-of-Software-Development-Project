import os
import random
import pickle  # For object serialization
import re 
from collections import defaultdict

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(1, 999999)).zfill(6)  # 6-digit unique ID
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def enroll_subject(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)
        else:
            print("You have already enrolled in the maximum number of subjects (4).")

    def drop_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)
        else:
            print("You are not enrolled in this subject.")

    def change_password(self, new_password):
        self.password = new_password

    def calculate_average_mark(self):
        if not self.subjects:
            return 0  # No subjects enrolled
        total_mark = sum(subject.mark for subject in self.subjects)
        return total_mark / len(self.subjects)

    def is_passing(self):
        return self.calculate_average_mark() >= 50
    
    def calculate_grade(self):
        mark = self.calculate_average_mark()
        if 90 <= mark <= 100:
            return 'A'
        elif 80 <= mark < 90:
            return 'B'
        elif 70 <= mark < 80:
            return 'C'
        elif 60 <= mark < 70:
            return 'D'
        else:
            return 'F'
   

class Utils:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PASSWORD_REGEX = r'^[A-Z][a-zA-Z0-9]{5,}[0-9]{3,}$'

class Subject:
    def __init__(self):
        self.id = str(random.randint(1, 999)).zfill(3)  # 3-digit unique ID
        self.mark = random.randint(25, 100)
        self.calculate_grade()

    def calculate_grade(self):
        if 90 <= self.mark <= 100:
            self.grade = 'A'
        elif 80 <= self.mark < 90:
            self.grade = 'B'
        elif 70 <= self.mark < 80:
            self.grade = 'C'
        elif 60 <= self.mark < 70:
            self.grade = 'D'
        else:
            self.grade = 'F'

class Database:
    @staticmethod
    def file_exists():
        return os.path.exists("students.data")

    @staticmethod
    def create_file():
        with open("students.data", "wb") as file:
            pickle.dump([], file)

    @staticmethod
    def write_objects(objects):
        with open("students.data", "wb") as file:
            pickle.dump(objects, file)

    @staticmethod
    def read_objects():
        if Database.file_exists():
            with open("students.data", "rb") as file:
                return pickle.load(file)
        return []  # Return an empty list if the file doesn't exist

    @staticmethod
    def clear_objects():
        with open("students.data", "wb") as file:
            pickle.dump([], file)

def save_students_to_file(students):
    Database.write_objects(students)

def main_menu():
    while True:
        print("University System: (A)dmin, (S)tudent, or X:")
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'A':
            admin_menu()
        elif choice == 'S':
            student_menu()
        elif choice == 'X':
            exit()
        else:
            print("Invalid choice. Please try again.")

def student_menu():
    while True:
        print("\nStudent System (L)ogin, (R)egister, or (X) Exit:")
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'L':
            student,students = student_login()
            if student:
                student_actions(student, students)
        elif choice == 'R':
            student_register()
        elif choice == 'X':
            print("Thank you.")
            main_menu()
        else:
            print("Invalid choice. Please try again.")

def student_login():
    # Implement the login functionality here and return the student object if login is successful
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    # Check if the login credentials are valid, and load the student object from the database
    students = Database.read_objects()
    for student in students:
        if student.email == email and student.password == password:
            print("Login successful.")
            return student,students

    print("Invalid credentials. Please try again.")
    return None,students

def student_actions(student, students):
    while True:
        print("\nStudent Course Menu (C)hange, (E)nrol, (R)emove, (S)how, or (X) Exit:")
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'C':
           while True:
            new_password = input("Enter a new password: ").strip()
            if re.match(Utils.PASSWORD_REGEX, new_password):
                print("Password is valid. Changing password...")
                break
            else:
                print("Invalid password format. Please try again.")
            save_students_to_file(students)  # Save students to the file after changing password
        elif choice == 'E':
            if len(student.subjects) >= 4:
                print("You have already enrolled in the maximum number of subjects (4).")
            else:
                subject = Subject()
                student.enroll_subject(subject)
                print("Enrolled in a subject.")
                save_students_to_file(students)  # Save students to the file after enrolling
        elif choice == 'R':
            if not student.subjects:
                print("You are not enrolled in any subjects.")
            else:
                subject_id = input("Enter the ID of the subject to remove: ").strip()
                for subject in student.subjects:
                    if subject.id == subject_id:
                        student.drop_subject(subject)
                        print("Subject removed.")
                        save_students_to_file(students)  # Save students to the file after removing
                        break
                else:
                    print("Subject not found in your enrollment.")
        elif choice == 'S':
            if not student.subjects:
                print("You are not enrolled in any subjects.")
            else:
                print("Enrolled Subjects:")
                for subject in student.subjects:
                    print(f"ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
        elif choice == 'X':
            student_menu()
        else:
            print("Invalid choice. Please try again.")

def admin_menu():
    while True:
        print("\nAdmin System (C)lear database file, (G)roup students, (P)artition students, (R)emove student, (S)how students, or (X) Exit:")
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'C':
            clear_database_file()
        elif choice == 'G':
            group_students()
        elif choice == 'P':
            partition_students()
        elif choice == 'R':
            remove_student()
        elif choice == 'S':
            show_students()
        elif choice == 'X':
            main_menu()
        else:
            print("Invalid choice. Please try again.")

def student_register():
    # Check if the 'students.data' file exists; if not, create it
    if not Database.file_exists():
        Database.create_file()

    while True:
        print("\nStudent Sign Up")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not re.match(Utils.EMAIL_REGEX, email) or not re.match(Utils.PASSWORD_REGEX, password):
            print("Incorrect email or password format. Please try again.")
            continue

        # Check if the email already exists in students.data
        students = Database.read_objects()
        for student in students:
            if student.email == email:
                print(f"Student {student.name} already exists.")
                student_menu()
                return

        name = input("Name: ").strip()
        print(f"Enrolling Student {name}")

        # Create a new student and save it to students.data
        student = Student(name, email, password)
        students.append(student)
        save_students_to_file(students)  # Save students to the file
        break

    print("Student registered successfully.")

def clear_database_file():
    Database.create_file()
    print("Database cleared successfully")
def group_students():
    students = Database.read_objects()  # Assuming Database provides a method to read student data
    grouped_students = defaultdict(list)

    for student in students:
        if  student.subjects:
            grade = student.calculate_grade()  # Assuming Student has a method for calculating grades
            grouped_students[grade].append(student)
            

    for grade, students in grouped_students.items():
        print(f"Grade {grade}:")
        for student in students:
            print(f"Student ID: {student.id}, Name: {student.name}")
    if len(grouped_students)==0:
        print("No suject enrolled or No student register")
    return grouped_students


def partition_students():
    # Implement the functionality to partition students by pass/fail
    pass

def remove_student():
    # Implement the functionality to remove a student by ID
    pass

def show_students():
    students = Database.read_objects()  # Assuming Database provides a method to read student data

    if not students:
        print("No students found in the database.")
    else:
        print("List of Students:")
        for student in students:
            print(f"Student ID: {student.id}")
            print(f"Name: {student.name}")
            print(f"Email: {student.email}")
            print("Subjects Enrolled:")
            if student.subjects:
                for subject in student.subjects:
                    print(f"Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
                    print("Average Mark:", student.calculate_average_mark())
                    print("Passing Status:", "Pass" if student.is_passing() else "Fail")
            else:
                print("No subjects enrolled.")
            print("-" * 20)  # Separating each student's information

    # Implement the functionality to show the list of students
    pass

if __name__ == "__main__":
    if not Database.file_exists():
        Database.create_file()
    main_menu()

# students=Database.read_objects()

# for student in students:
#     print(f"Student ID: {student.id}")
#     print(f"Name: {student.name}")
#     print(f"Email: {student.email}")
#     print(f"Password: {student.password}")
#     print(f"Subjects: {student.subjects}")
#     print()