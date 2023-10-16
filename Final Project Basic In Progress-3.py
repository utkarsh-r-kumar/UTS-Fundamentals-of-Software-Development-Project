import os
import random
import pickle
import re 

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(1, 999999)).zfill(6)  # 6-digit unique ID
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []
        self.overall_mark = 0  # Initialize overall mark to 0

    def enroll_subject(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)
            self.calculate_overall_mark()  # Calculate overall mark
        else:
            print("You have already enrolled in the maximum number of subjects (4).")

    def change_password(self, new_password):
        self.password = new_password

    def drop_subject(self, subject_id):
        subject_to_remove = None
        for subject in self.subjects:
            if subject.id == subject_id:
                subject_to_remove = subject
                break

        if subject_to_remove:
            self.subjects.remove(subject_to_remove)
            self.calculate_overall_mark()  # Calculate overall mark
            print(f"Subject-{subject_id} removed.")
        else:
            print(f"Not enrolled in Subject-{subject_id}")

    def calculate_overall_mark(self):
        if not self.subjects:
            self.overall_mark = 0
        else:
            total_mark = sum(subject.mark for subject in self.subjects)
            self.overall_mark = total_mark / len(self.subjects)
    def is_passing(self):
        # check if they pass individual subject. If they are fail in one subject they should be markerd as fail
        for subject in self.subjects:
            if subject.mark < 50:
                return False
        #sometime student might be registered but, they might not have been enrolled so we need to check overall marks as well
        if(self.overall_mark >= 50):
            return True
        else: 
            return False


class Utils:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PASSWORD_REGEX = r'^[A-Z][a-zA-Z0-9]{5,}[0-9]{3,}$'

class Subject:
    def __init__(self):
        self.id = str(random.randint(1, 999)).zfill(3)  # 3-digit unique ID
        self.mark = random.randint(25, 100)
        self.calculate_grade()

    def calculate_grade(self):
        if 85 <= self.mark <= 100:
            self.grade = 'HD'
        elif 75 <= self.mark < 85:
            self.grade = 'D'
        elif 65 <= self.mark < 75:
            self.grade = 'C'
        elif 50 <= self.mark < 65:
            self.grade = 'P'
        else:
            self.grade = 'Z'

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
        print("University System: (A)dmin, (S)tudent, or Exit(X):")
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
            student = student_login()
            if student:
                student_actions(student)
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
            return student

    print("Invalid credentials. Please try again.")
    return None

def student_actions(student):
    while True:
        print("\nStudent Course Menu (C)hange, (E)nrol, (R)emove, (S)how, or (X) Exit:")
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'C':
            new_password = input("Enter a new password: ").strip()
            student.change_password(new_password)
            print("Password changed successfully.")
            save_students_to_file([student])  # Save the updated student to the file after changing password
        elif choice == 'E':
            if len(student.subjects) >= 4:
                print("You are allowed to enroll in a maximum of 4 subjects only.")
            else:
                subject = Subject()
                student.enroll_subject(subject)
                print(f"Enrolled in Subject-{subject.id}")
                save_students_to_file([student])  # Save the updated student to the file after enrolling
        elif choice == 'R':
            if not student.subjects:
                print("You are not enrolled in any subjects.")
            else:
                subject_id = input("Remove Subject by ID: ").strip()
                student.drop_subject(subject_id)
                save_students_to_file([student])  # Save the updated student to the file after removing
        elif choice == 'S':
            if not student.subjects:
                print("You are not enrolled in any subjects.")
            else:
                print("Enrolled Subjects:")
                for subject in student.subjects:
                    print(f"[Subject::{subject.id} -- mark = {subject.mark} -- grade = {subject.grade}]")
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
    print("Clearing students database")
    choice = input("Are you sure you want to clear the database (Y)ES/(N)O: ").strip().upper()
    
    if choice == 'Y':
        Database.clear_objects()
        print("Students data cleared")
    elif choice == 'N':
        pass
    else:
        print("Invalid choice. Please enter 'Y' for Yes or 'N' for No.")

def group_students():
    students = Database.read_objects()  # Assuming Database provides a method to read student data
    print("Grade Grouping")
    if not students:
        print("< Nothing to Display >")
    else:
        grouped_students = defaultdict(list)

        for student in students:
            if student.subjects:
                grade = student.calculate_grade()  # Assuming Student has a method for calculating grades
                grouped_students[grade].append(student)

        for grade, students in grouped_students.items():
            print(f"{grade} --> {[student.name + ' :: ' + student.id + ' --> GRADE: ' + student.calculate_grade() + ' - MARK: ' + str(student.calculate_average_mark()) for student in students]}")



def partition_students():
    students = Database.read_objects()  

    passing_students = []
    failing_students = []

    for student in students:
        if student.is_passing():
            passing_students.append(student)
        else:
            failing_students.append(student)

    print("PASS/FAIL Partition")
    print(f"FAIL --> {[student.name + ' :: ' + student.id + ' --> GRADE: ' + student.calculate_grade() + ' - MARK: ' + str(student.calculate_average_mark()) for student in failing_students]}")
    print(f"PASS --> {[student.name + ' :: ' + student.id + ' --> GRADE: ' + student.calculate_grade() + ' - MARK: ' + str(student.calculate_average_mark()) for student in passing_students]}")


def remove_student():
    #Binaya
    # Implement the functionality to remove a student by ID
    student_id = input("Enter the ID of the student to remove: ").strip()
    students = Database.read_objects()

    for student in students:
        if student.id == student_id:
            students.remove(student)
            Database.write_objects(students)
            print(f"Student with ID {student_id} removed successfully.")
            return

    print(f"No student found with ID {student_id}.")
    

def show_students():
    students = Database.read_objects()  
    print("Student List")
    if not students:
        print("< Nothing to Display >")
    else:
        for student in students:
            print(f"{student.name} :: {student.id} --> Email: {student.email}")


if __name__ == "__main__":
    if not Database.file_exists():
        Database.create_file()
    main_menu()
