import tkinter as tk
from tkinter import messagebox
import os
import random
import pickle
import re
from collections import defaultdict

class Subject:
    def __init__(self, id, mark, grade):
        self.id = id
        self.mark = mark
        self.grade = grade

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
            messagebox.showerror("Error", "You have already enrolled in the maximum number of subjects (4).")

    def drop_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)
        else:
            messagebox.showerror("Error", "You are not enrolled in this subject.")

    def calculate_average_mark(self):
        if not self.subjects:
            return 0  # No subjects enrolled
        total_mark = sum(subject.mark for subject in self.subjects)
        return total_mark / len(self.subjects)

    def is_passing(self):
        # Check if they pass individual subjects. If they fail in one subject, they should be marked as fail
        for subject in self.subjects:
            if subject.mark < 50:
                return False
        # Sometimes students might be registered but not have been enrolled, so we need to check overall marks as well
        if self.calculate_average_mark() >= 50:
            return True
        else:
            return False


class Utils:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zAZ0-9-.]+$'
    PASSWORD_REGEX = r'^[A-Z][a-zA-Z0-9]{5,}[0-9]{3,}$'


class Database:
    @staticmethod
    def file_exists(filename):
        return os.path.exists(filename)

    @staticmethod
    def create_file(filename):
        with open(filename, "wb") as file:
            pickle.dump([], file)

    @staticmethod
    def write_objects(objects, filename):
        with open(filename, "wb") as file:
            pickle.dump(objects, file)

    @staticmethod
    def read_objects(filename):
        if Database.file_exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
        return []  # Return an empty list if the file doesn't exist

    @staticmethod
    def save_students_to_file(students):
        Database.write_objects(students, "students.data")

    @staticmethod
    def save_subjects_to_file(subjects):
        Database.write_objects(subjects, "students.data")  # Use the same file as CLI for subjects


class StudentSystemApp:
    def __init__(self, root):
        self.root = root
        self.students = []
        self.load_students()  # Load students from the same file as CLI
        self.main_menu()
        self.current_student = None

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_students(self):
        self.students = Database.read_objects("students.data")  # Load students from the same file as CLI

    def save_students(self):
        Database.save_students_to_file(self.students)  # Save students to the same file as CLI

    def main_menu(self):
        self.clear_screen()
        self.root.title("University System")
        self.root.geometry("300x200")
        self.root.configure(bg='#607b8d')
        self.root.resizable(False, False)

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
        student_login_label = tk.Label(self.root, text="Student Login", bg='#607b8d')
        student_login_label.pack()
        email_label = tk.Label(self.root, text="Email:", bg='#607b8d')
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:", bg='#607b8d')
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        password_entry.pack()

        login_button = tk.Button(self.root, text="Login", command=lambda: self.login_action(email_entry.get(), password_entry.get()))
        login_button.pack(side="right")

        back_button = tk.Button(self.root, text="Back", command=self.student_menu)
        back_button.pack(side="right")

    def login_action(self, email, password):
        # Check if the email and password exist in students.data
        found_student = None
        for student in self.students:
            if student.email == email and student.password == password:
                found_student = student
                break

        if found_student is not None:
            messagebox.showinfo("Success", "Login successful.")
            self.current_student = found_student
            self.student_actions(found_student)
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    def student_actions(self, student):
        self.clear_screen()
        course_menu_label = tk.Label(self.root, text="Student Course Menu", bg='#607b8d')
        course_menu_label.pack()
        change_password_button = tk.Button(self.root, text="Change Password", command=lambda: self.change_password(student))
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
        change_password_label = tk.Label(self.root, text="Change Password", bg='#607b8d')
        change_password_label.pack()
        new_password_label = tk.Label(self.root, text="Enter a new password:", bg='#607b8d')
        new_password_label.pack()
        new_password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        new_password_entry.pack()
        change_password_button = tk.Button(self.root, text="Change Password",
                                          command=lambda: self.update_password(new_password_entry.get()))
        change_password_button.pack(side="right")
        back_button = tk.Button(self.root, text="Back", command=lambda: self.student_actions(student))
        back_button.pack(side="right")

    def update_password(self, new_password):
        # Validate the new password and update the student's password
        for index, student in enumerate(self.students):
            if student.id == self.current_student.id:
                if not re.match(Utils.PASSWORD_REGEX, new_password):
                    messagebox.showerror("Error", "Incorrect password format. Please try again.")
                else:
                    self.current_student.password = new_password
                    self.students[index] = self.current_student
                    self.save_students()  # Save students to the file after changing the password
                    messagebox.showinfo("Success", "Password changed successfully.")
                break

    def enroll_subject(self):
        self.clear_screen()

        # Check if the student has already enrolled in the maximum number of subjects
        if len(self.current_student.subjects) >= 4:
            messagebox.showerror("Error", "You have already enrolled in the maximum number of subjects (4).")
        else:
            # Generate a random subject ID from Subject-000 to Subject-999
            subject_id = f"Subject-{str(random.randint(0, 999)).zfill(3)}"

            # Enroll the student in the randomly generated subject
            self.current_student.enroll_subject(Subject(subject_id, 0))  # Assigning a mark of 0, but we won't use it

            # Show a message to indicate the enrollment
            messagebox.showinfo("Enrollment", f"Enrolled in {subject_id}.")

        back_button = tk.Button(self.root, text="Back", command=lambda: self.student_actions(self.current_student))
        back_button.pack(side="right")

    def remove_subject(self):
        self.clear_screen()
        remove_subject_label = tk.Label(self.root, text="Remove Subject", bg='#607b8d')
        remove_subject_label.pack()

        subject_code_label = tk.Label(self.root, text="Subject Code (e.g., 001):", bg='#607b8d')
        subject_code_label.pack()

        subject_code_entry = tk.Entry(self.root)
        subject_code_entry.pack()

        remove_button = tk.Button(self.root, text="Remove", command=lambda: self.remove_action(subject_code_entry.get()))
        remove_button.pack(side="right")

        back_button = tk.Button(self.root, text="Back", command=lambda: self.student_actions(self.current_student))
        back_button.pack(side="right")

    def remove_action(self, subject_code):
        # Validate subject removal and remove it from the student's subjects
        if not re.match(r'^\d{3}$', subject_code):
            messagebox.showerror("Error", "Invalid subject code. Please enter 3 digits (e.g., 001).")
            return

        subject_id = f"Subject-{subject_code}"
        subject = next((s for s in self.current_student.subjects if s.name == subject_id), None)

        if subject:
            self.current_student.drop_subject(subject)
            students = self.students
            for index, student in enumerate(students):
                if student.id == self.current_student.id:
                    students[index] = self.current_student
                    self.save_students()  # Save students to the file after removing the subject
                    messagebox.showinfo("Success", f"Removed subject: {subject_id}.")
                    break
        else:
            messagebox.showerror("Error", f"You are not enrolled in subject {subject_id}.")

    def show_subjects(self):
        self.clear_screen()
        show_subjects_label = tk.Label(self.root, text="Enrolled Subjects", bg='#607b8d')
        show_subjects_label.pack()
        subjects_text = "Enrolled Subjects:\n"
        for subject in self.current_student.subjects:
            subject_info = f"Subject-{subject.id} -- mark = {subject.mark} -- grade = {subject.grade}"
            subjects_text += subject_info + "\n"
        subjects_label = tk.Label(self.root, text=subjects_text, bg='#607b8d', justify='left')
        subjects_label.pack()

        back_button = tk.Button(self.root, text="Back", command=lambda: self.student_actions(self.current_student))
        back_button.pack()

    def student_register(self):
        self.clear_screen()
        student_register_label = tk.Label(self.root, text="Student Register", bg='#607b8d')
        student_register_label.pack()
        email_label = tk.Label(self.root, text="Email:", bg='#607b8d')
        email_label.pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:", bg='#607b8d')
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")  # To hide the password characters
        password_entry.pack()

        name_label = tk.Label(self.root, text="Name:", bg='#607b8d')
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        register_button = tk.Button(self.root, text="Register",
                                    command=lambda: self.register_action(email_entry.get(), password_entry.get(), name_entry.get()))
        register_button.pack(side="right")

        back_button = tk.Button(self.root, text="Back", command=self.student_menu)
        back_button.pack(side="right")

    def register_action(self, email, password, name):
        if not re.match(Utils.EMAIL_REGEX, email) or not re.match(Utils.PASSWORD_REGEX, password):
            messagebox.showerror("Error", "Incorrect email or password format. Please try again.")
            return
        # Check if the email already exists in students.data
        for student in self.students:
            if student.email == email:
                messagebox.showerror("Error", f"Student {student.name} already exists.")
                return
        # Create a new student and save it to students.data
        student = Student(name, email, password)
        self.students.append(student)
        self.save_students()  # Save students to the file
        messagebox.showinfo("Success", f"Enrolling Student {name}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentSystemApp(root)
    root.mainloop()
