import tkinter as tk
from tkinter import messagebox
import os
import random
import pickle  # For object serialization
import re
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

    def calculate_average_mark(self):
        if not self.subjects:
            return 0  # No subjects enrolled
        total_mark = sum(subject.mark for subject in self.subjects)
        return total_mark / len(self.subjects)

    def is_passing(self):
        # check if they pass individual subject. If they are fail in one subject they should be markerd as fail
        for subject in self.subjects:
            if subject.mark < 50:
                return False
        #sometime student might be registered but, they might not have been enrolled so we need to check overall marks as well
        if(self.calculate_average_mark() >= 50):
            return True
        else: 
            return False
class Utils:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PASSWORD_REGEX = r'^[A-Z][a-zA-Z0-9]{5,}[0-9]{3,}$'
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


class StudentSystemApp:
    def __init__(self, root):
        self.root = root
        self.students = []
        self.main_menu()
        self.current_student = None
    def main_menu(self):
        self.clear_screen()
        self.root.title("University System")
        self.root.geometry("300x200")
        self.root.configure(bg='#607b8d')
        self.root.resizable(False, False)
        admin_button = tk.Button(self.root, text="Admin", command=self.admin_menu)
        admin_button.pack()
        student_button = tk.Button(self.root, text="Student", command=self.student_menu)
        student_button.pack()
        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack()

    def student_menu(self):
        self.clear_screen()
        self.root.title("Student System")
        login_button = tk.Button(self.root, text="Login", command=self.student_login)
        login_button.pack()
        register_button = tk.Button(self.root, text="Register", command=self.student_register)
        register_button.pack()
        exit_button = tk.Button(self.root, text="Exit", command=self.main_menu)
        exit_button.pack()

    def student_login(self):
        self.clear_screen()
        student_login_label = tk.Label(self.root, text="Student Login",bg='#607b8d')
        student_login_label.pack()
        email_label = tk.Label(self.root, text="Email:",bg='#607b8d')
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:",bg='#607b8d')
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        password_entry.pack()

        login_button = tk.Button(self.root, text="Login", command=lambda: self.login_action(email_entry.get(), password_entry.get()))
        login_button.pack(side="right")

        back_button = tk.Button(self.root, text="Back", command=self.student_menu)
        back_button.pack(side="right")

    def login_action(self, email, password):
            # Check if the email and password exist in students.data
        students = Database.read_objects()
        found_student = None
        for student in students:
            if student.email == email and student.password == password:
                found_student = student
                break

        if found_student!=None:
            messagebox.showinfo("Success", "Login successful.")
            self.current_student = found_student
            self.student_actions(found_student)
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    def student_actions(self,student):
        self.clear_screen()
        course_menu_label = tk.Label(self.root, text="Student Course Menu",bg='#607b8d')
        course_menu_label.pack()
        change_password_button = tk.Button(self.root, text="Change Password", command=lambda:self.change_password(student))
        change_password_button.pack()

        enroll_button = tk.Button(self.root, text="Enroll in Subject", command=self.enroll_subject)
        enroll_button.pack()

        remove_button = tk.Button(self.root, text="Remove Subject", command=self.remove_subject)
        remove_button.pack()

        show_button = tk.Button(self.root, text="Show Enrolled Subjects", command=self.show_subjects)
        show_button.pack()

        back_button = tk.Button(self.root, text="Back", command=self.student_login)
        back_button.pack()

    def change_password(self, student):
        self.clear_screen()
        change_password_label = tk.Label(self.root, text="Change Password",  bg='#607b8d')
        change_password_label.pack()
        new_password_label = tk.Label(self.root, text="Enter a new password:", bg='#607b8d')
        new_password_label.pack()
        new_password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        new_password_entry.pack()
        change_password_button = tk.Button(self.root, text="Change Password", command=lambda:self.update_password(new_password_entry.get()))
        change_password_button.pack(side="right")
        back_button = tk.Button(self.root, text="Back", command=lambda: self.student_actions(student))
        back_button.pack(side="right")

    def update_password(self, new_password):
    # Validate the new password and update the student's password
        students=Database.read_objects()
        for index, student in enumerate(students):
                if student.id == self.current_student.id:
                    if not re.match(Utils.PASSWORD_REGEX, new_password):
                        messagebox.showerror("Error", "Incorrect password format. Please try again.")
                    else:
                        self.current_student.password = new_password
                        students[index] = self.current_student
                        Database.save_students_to_file(students) # Save students to the file after changing password
                        messagebox.showinfo("Success", "Password changed successfully.")
                    break

    def enroll_subject(self):
        # Implement the enrollment of subjects here using a similar approach as change_password
        pass  # Add your implementation here

    def remove_subject(self):
    # Implement the removal of subjects here using a similar approach as change_password
        pass  # Add your implementation here

    def show_subjects(self):
    # Implement displaying enrolled subjects using a similar approach as change_password
        pass  # Add your implementation here

    def student_register(self):
        self.clear_screen()
        student_register_label = tk.Label(self.root, text="Student Register",bg='#607b8d')
        student_register_label.pack()
        email_label = tk.Label(self.root, text="Email:",bg='#607b8d')
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:",bg='#607b8d')
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        password_entry.pack()

        name_label = tk.Label(self.root, text="Name:",bg='#607b8d')
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        register_button = tk.Button(self.root, text="Register", command=lambda: self.register_action(email_entry.get(), password_entry.get(),name_entry.get()))
        register_button.pack(side="right")

        back_button = tk.Button(self.root, text="Back", command=self.student_menu)
        back_button.pack(side="right")
    def register_action(self,email, password,name):
        students = Database.read_objects()
        if not Database.file_exists():
            Database.create_file()
        if not re.match(Utils.EMAIL_REGEX, email) or not re.match(Utils.PASSWORD_REGEX, password):
            messagebox.showerror("Error","Incorrect email or password format. Please try again.")
            return
        # Check if the email already exists in students.data
        for student in students:
            if student.email == email:
                messagebox.showerror("Error",f"Student {student.name} already exists.")
                return
                # Create a new student and save it to students.data

        student = Student(name, email, password)
        students.append(student)
        Database.save_students_to_file(students)  # Save students to the file
        messagebox.showinfo("Success",f"Enrolling Student {name}")

            

    def admin_menu(self):
        self.clear_screen()

        root.title("Admin System")

        clear_button = tk.Button(self.root, text="Clear Database", command=self.clear_database_file)
        clear_button.pack()
        group_button = tk.Button(self.root, text="Group Students", command=self.group_students)
        group_button.pack()
        partition_button = tk.Button(self.root, text="Partition Students", command=self.partition_students)
        partition_button.pack()
        remove_button = tk.Button(self.root, text="Remove Student", command=self.remove_student)
        remove_button.pack()
        show_button = tk.Button(self.root, text="Show Students", command=self.show_students)
        show_button.pack()
        exit_button = tk.Button(self.root, text="Exit", command=self.main_menu)
        exit_button.pack()

    def clear_database_file(self):
        # Implement the clear database functionality using tkinter
        pass

    def group_students(self):
        # Implement the group students functionality using tkinter
        pass

    def partition_students(self):
        # Implement the partition students functionality using tkinter
        pass

    def remove_student(self):
        # Implement the remove student functionality using tkinter
        pass

    def show_students(self):
        # Implement the show students functionality using tkinter
        pass

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    if not Database.file_exists():
        Database.create_file()
    root = tk.Tk()
    app = StudentSystemApp(root)
    root.mainloop()


