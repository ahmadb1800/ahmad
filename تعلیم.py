import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import hashlib
import json

# صفحه ورود
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("صفحه ورود")
        self.root.geometry("400x300")

        # برچسب عنوان
        title_label = tk.Label(self.root, text="ورود به سیستم آموزشی", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # انتخاب نقش
        self.role_var = tk.StringVar(value="دانشجو")

        student_radio = tk.Radiobutton(self.root, text="دانشجو", variable=self.role_var, value="دانشجو", font=("Arial", 14))
        teacher_radio = tk.Radiobutton(self.root, text="استاد", variable=self.role_var, value="استاد", font=("Arial", 14))
        student_radio.pack(pady=5)
        teacher_radio.pack(pady=5)

        # فیلد کد کلاس
        self.class_code_entry = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.class_code_entry.pack(pady=10)

        # دکمه ورود
        login_button = tk.Button(self.root, text="ورود", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        role = self.role_var.get()
        class_code = self.class_code_entry.get()

        if role == "دانشجو":
            # احراز هویت دانشجو
            student_data = self.authenticate_student(class_code)
            if student_data:
                self.root.destroy()
                root = tk.Tk()
                StudentUI(root, student_data)
            else:
                messagebox.showerror("خطا", "کد کلاس اشتباه یا دانشجو وجود ندارد.")
        elif role == "استاد":
            # احراز هویت استاد
            teacher_data = self.authenticate_teacher(class_code)
            if teacher_data:
                self.root.destroy()
                root = tk.Tk()
                TeacherUI(root, teacher_data)
            else:
                messagebox.showerror("خطا", "کد کلاس اشتباه یا استاد وجود ندارد.")

    def authenticate_student(self, class_code):
        # ... احراز هویت دانشجو با استفاده از class_code
        try:
            with open('class_data.json', 'r') as f:
                class_data = json.load(f)
            if class_code in class_data:
                if "students" in class_data[class_code]:
                    return class_data[class_code]["students"]
        except FileNotFoundError:
            pass
        return None

    def authenticate_teacher(self, class_code):
        # ... احراز هویت استاد با استفاده از class_code
        try:
            with open('class_data.json', 'r') as f:
                class_data = json.load(f)
            if class_code in class_data:
                if "teacher" in class_data[class_code]:
                    return class_data[class_code]["teacher"]
        except FileNotFoundError:
            pass
        return None

# رابط کاربری دانشجو و استاد (قالب مشترک)
class UserInterface:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        if isinstance(user_data, list):  # دانشجو
            self.root.title("پنل دانشجو")
        else:  # استاد
            self.root.title("پنل استاد")
        self.root.geometry("600x400")

        # ... کد مشترک برای دانشجو و استاد
        self.class_code_label = tk.Label(self.root, text=f"کد کلاس: {self.get_class_code(user_data)}", font=("Arial", 14))
        self.class_code_label.pack(pady=10)

    def get_class_code(self, user_data):
        # ...  خارج کردن کد کلاس از user_data
        if isinstance(user_data, list):  # دانشجو
            return user_data[0]
        else:  # استاد
            return user_data["class_code"]

# رابط کاربری دانشجو
class StudentUI(UserInterface):
    def __init__(self, root, student_data):
        super().__init__(root, student_data)

        # ... کد مخصوص دانشجو

# رابط کاربری استاد
class TeacherUI(UserInterface):
    def __init__(self, root, teacher_data):
        super().__init__(root, teacher_data)

        # ایجاد کلاس جدید
        create_class_button = tk.Button(self.root, text="ایجاد کلاس جدید", font=("Arial", 14), bg="#2196F3", fg="white", command=self.create_class)
        create_class_button.pack(pady=10, fill=tk.X, padx=20)

    def create_class(self):
        class_name = simpledialog.askstring("نام کلاس", "نام کلاس را وارد کنید:")
        if class_name:
            # ایجاد کد کلاس منحصر به فرد
            class_code = self.generate_class_code(class_name)
            messagebox.showinfo("کد کلاس", f"کد کلاس: {class_code}")
            # ذخیره اطلاعات کلاس
            self.save_class(class_name, class_code)

    def generate_class_code(self, class_name):
        # ...  تولید کد کلاس منحصر به فرد
        class_code = hashlib.sha256(class_name.encode()).hexdigest()[:8]
        return class_code

    def save_class(self, class_name, class_code):
        # ...  ذخیره اطلاعات کلاس
        try:
            with open('class_data.json', 'r') as f:
                class_data = json.load(f)
        except FileNotFoundError:
            class_data = {}
        class_data[class_code] = {
            "name": class_name,
            "teacher": "teacher_id",  #  You need to handle this
            "students": []
        }
        with open('class_data.json', 'w') as f:
            json.dump(class_data, f)

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
