import tkinter as tk 
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import mysql.connector

window = tk.Tk()

window.state("zoomed")
header_frame = tk.Frame( bg="#f5f7fb")
header_frame.pack(fill='x', padx=20, pady=10)
tk.Label(header_frame, text="IT Department Management System", font=("Segoe UI", 30, "bold"), 
         bg="#f5f7fb", fg="#333").pack(side='top', anchor='n', pady=(0, 5))

notebook = ttk.Notebook()
notebook.pack(fill='both', expand=True, padx=10, pady=10)

_1stYearStudent = ttk.Frame(notebook)
_2ndYearStudent = ttk.Frame(notebook)
_3rYearStudent = ttk.Frame(notebook)
attendance = ttk.Frame(notebook)
staff_tab = ttk.Frame(notebook)
# settings_tab = ttk.Frame(notebook)

notebook.add(_1stYearStudent, text='1st Year Students ')
notebook.add(_2ndYearStudent, text="2nd Year Students ")
notebook.add(_3rYearStudent, text="3rd Year Studednts ")
notebook.add(attendance, text="Attendance")
notebook.add(staff_tab, text='Staff ')
# notebook.add(settings_tab, text='Settings')

#----------------- Add Student Function ----------------#
def add_student():
    add_std_win = tk.Toplevel()
    add_std_win.geometry("600x400")
    add_std_win.title("Add Student")

    heading = tk.Label(add_std_win, text="Add Student", font=("Segoe UI", 20, "bold"))
    heading.grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(add_std_win, text="Student Name:", font=("Segoe UI", 10)).grid(row=1, column=0, 
                                                                            padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(add_std_win, width=25)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_std_win, text="Email:", font=("Segoe UI", 10)).grid(row=2, column=0, padx=10, 
                                                                     pady=5, sticky="e")
    email_entry = tk.Entry(add_std_win, width=25)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_std_win, text="Address:", font=("Segoe UI", 10)).grid(row=3, column=0, padx=10,
                                                                        pady=5, sticky="e")
    address_entry = tk.Entry(add_std_win, width=25)
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    # tk.Label(add_std_win, text="Gender:", font=("Segoe UI", 10)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    # gender_entry = tk.Entry(add_std_win, width=25)
    # gender_entry.grid(row=4, column=1, padx=10, pady=5)
    tk.Label(add_std_win, text="Gender:", font=("Segoe UI", 10)).grid(row=4, column=0, padx=10, 
                                                                      pady=5, sticky="e")
    gender_var = tk.StringVar(value="Male")  # default value
    tk.Radiobutton(add_std_win, text="Male", variable=gender_var, value="Male", 
                   bg="white").grid(row=4, column=1, sticky="w")
    tk.Radiobutton(add_std_win, text="Female", variable=gender_var, value="Female", 
                   bg="white").grid(row=4, column=1, padx=80, sticky="w")
    tk.Radiobutton(add_std_win, text="Other", variable=gender_var, value="Other", 
                   bg="white").grid(row=4, column=1, padx=160, sticky="w")

    tk.Label(add_std_win, text="Date of Birth (YYYY-MM-DD):", 
             font=("Segoe UI", 10)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    dob_entry = tk.Entry(add_std_win, width=25)
    dob_entry.grid(row=5, column=1, padx=10, pady=5)

    # tk.Label(add_std_win, text="Year:", font=("Segoe UI", 10)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    # year_entry = tk.Entry(add_std_win, width=25)
    # year_entry.grid(row=6, column=1, padx=10, pady=5)
    tk.Label(add_std_win, text="Year:", font=("Segoe UI", 10)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    year_var = tk.IntVar(value=1)  # default value
    tk.Radiobutton(add_std_win, text="1st Year", variable=year_var, value=1,
                    bg="white").grid(row=6, column=1, sticky="w")
    tk.Radiobutton(add_std_win, text="2nd Year", variable=year_var, value=2, 
                   bg="white").grid(row=6, column=1, padx=80, sticky="w")
    tk.Radiobutton(add_std_win, text="3rd Year", variable=year_var, value=3, 
                   bg="white").grid(row=6, column=1, padx=160, sticky="w")


    def save_student():
        name = name_entry.get()
        contact = email_entry.get()
        address = address_entry.get()
        # gender = gender_entry.get()
        gender = gender_var.get()
        dob = dob_entry.get()
        year = year_var.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mkkapri",
                database="studentManagement"
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student (name, contact, address, gender, dob, year)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, contact, address, gender, dob, year))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            add_std_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student.\n{e}")

    add_btn = tk.Button(add_std_win, text="+Add Student", font=("Segoe UI", 10, "bold"), 
                        bg="#4FC3F7", fg="black", padx=10, pady=5, bd=0, 
                        activebackground="#0288d1", activeforeground="white", 
                        command=save_student)
    add_btn.grid(row=7, column=0, columnspan=2, pady=20)

#-------------- Get Student to show in window -------------------#
def load_students_by_year(year, tree):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mkkapri",
            database="studentManagement"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, contact, address FROM student WHERE year = %s", (year,))
        records = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)
        for row in records:
            tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], "See More"))

        cursor.close()
        conn.close()
    except Exception as e:
        print("Error loading students:", e)


# ------- 1st Year student Tab ------- #
top_frame = tk.Frame(_1stYearStudent, bg="white")
top_frame.pack(fill="x", padx=10, pady=5)

tk.Label(top_frame, text="1St Year Student", font=("Segoe UI", 16, "bold"),
          bg="white").pack(side="left", padx=(0, 10))

add_student_btn = tk.Button(top_frame, text="+Add Student",  command=add_student ,font=("Segoe UI", 10, "bold"), 
                            bg="#4FC3F7", fg="black", padx=10, pady=5, bd=0, activebackground="#0288d1", 
                            activeforeground="white")
add_student_btn.pack(side="right", padx=10)

main_frame = tk.Frame(_1stYearStudent, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

student_table_1 = ttk.Treeview(main_frame, columns=("student ID", "Name", 
                                                    "Contact", "Address", "See More"), show="headings", height=10)
for col in ("student ID", "Name", "Contact", "Address", "See More"):
    student_table_1.heading(col, text=col)
    student_table_1.column(col, anchor="center", width=80)
student_table_1.pack(fill="both", expand=True, padx=10, pady=(0, 10))



#------------------2nd Year Student ------------------#
top_frame = tk.Frame(_2ndYearStudent, bg="white")
top_frame.pack(fill="x", padx=10, pady=5)

tk.Label(top_frame, text="2nd Year Student", font=("Segoe UI", 16, "bold"), 
         bg="white").pack(side="left", padx=(0, 10))

add_student_btn = tk.Button(top_frame, text="+Add Student" ,  command=add_student, 
                            font=("Segoe UI", 10, "bold"), bg="#4FC3F7", fg="black", 
                            padx=10, pady=5, bd=0, activebackground="#0288d1", activeforeground="white")
add_student_btn.pack(side="right", padx=10)

main_frame = tk.Frame(_2ndYearStudent, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

student_table_2 = ttk.Treeview(main_frame, columns=("student ID", "Name", "Contact", 
                                                    "Address", "See More"), show="headings", height=10)
for col in ("student ID", "Name", "Contact", "Address", "See More"):
    student_table_2.heading(col, text=col)
    student_table_2.column(col, anchor="center", width=80)
student_table_2.pack(fill="both", expand=True, padx=10, pady=(0, 10))


#------------------- 3rd Year Student----------------------#
top_frame = tk.Frame(_3rYearStudent, bg="white")
top_frame.pack(fill="x", padx=10, pady=5)

add_student_btn = tk.Button(top_frame, text="+Add Student" ,  command=add_student, 
                            font=("Segoe UI", 10, "bold"), bg="#4FC3F7", 
                            fg="black", padx=10, pady=5, bd=0, activebackground="#0288d1", 
                            activeforeground="white")
add_student_btn.pack(side="right", padx=10)

main_frame = tk.Frame(_3rYearStudent, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(top_frame, text="3rd Year Student", font=("Segoe UI", 16, "bold"), 
         bg="white").pack(side="left", padx=(0, 10))

student_table_3 = ttk.Treeview(main_frame, columns=("student ID", "Name", 
                                                    "Contact", "Address", "See More"), show="headings", height=10)
for col in ("student ID", "Name", "Contact", "Address", "See More"):
    student_table_3.heading(col, text=col)
    student_table_3.column(col, anchor="center", width=80)
student_table_3.pack(fill="both", expand=True, padx=10, pady=(0, 10))

load_students_by_year(1, student_table_1)
load_students_by_year(2, student_table_2)
load_students_by_year(3, student_table_3)

#---------------- Attendance -------------------------



#---------------------- Staff ---------------------------
def add_staff():
    add_staff_win = tk.Toplevel()
    add_staff_win.geometry("400x400")
    add_staff_win.title("Add Staff")

    heading = tk.Label(add_staff_win, text="Add Staff", font=("Segoe UI", 20, "bold"))
    heading.grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(add_staff_win, text="Staff Name:", 
             font=("Segoe UI", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(add_staff_win, width=25)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_staff_win, text="Email:", 
             font=("Segoe UI", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(add_staff_win, width=25)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_staff_win, text="Designation:",
              font=("Segoe UI", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    designation_entry = tk.Entry(add_staff_win, width=25)
    designation_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_staff_win, text="Phone:", 
             font=("Segoe UI", 10)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    phone_entry = tk.Entry(add_staff_win, width=25)
    phone_entry.grid(row=4, column=1, padx=10, pady=5)

    def save_staff():
        name = name_entry.get()
        email = email_entry.get()
        designation = designation_entry.get()
        phone = phone_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mkkapri",
                database="studentManagement"
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO staff (name, email, designation, phone)
                VALUES (%s, %s, %s, %s)
            """, (name, email, designation, phone))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Staff added successfully!")
            add_staff_win.destroy()
        except Exception as e:
            print("error log staff:", e)
        

    add_btn = tk.Button(add_staff_win, text="+Add Staff", font=("Segoe UI", 10, "bold"), 
                        bg="#4FC3F7", fg="black", padx=10, pady=5, bd=0, 
                        activebackground="#0288d1", activeforeground="white", 
                        command=save_staff)
    add_btn.grid(row=5, column=0, columnspan=2, pady=20)

def show_staff(tree):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mkkapri",
            database="studentManagement"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT staff_id, name, email, designation FROM staff")
        records = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)
        for row in records:
            tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], "See More"))

        cursor.close()
        conn.close()
    except Exception as e:
        print("Error loading Staff:", e)



top_frame = tk.Frame(staff_tab, bg="white")
top_frame.pack(fill="x", padx=10, pady=5)

tk.Label(top_frame, text="Staff", font=("Segoe UI", 16, "bold"), bg="white").pack(side="left", padx=(0, 10))

add_staff_btn = tk.Button(top_frame, text="+Add Staff" ,  command=add_staff, 
                          font=("Segoe UI", 10, "bold"), bg="#4FC3F7", 
                          fg="black", padx=10, pady=5, bd=0, activebackground="#0288d1", 
                          activeforeground="white")
add_staff_btn.pack(side="right", padx=10)

main_frame = tk.Frame(staff_tab, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

staff_table = ttk.Treeview(main_frame, columns=("Staff ID", "Name", "Email", 
                                                "Designation", "See More"), show="headings", height=10)
for col in ("Staff ID", "Name", "Email", "Designation", "See More"):
    staff_table.heading(col, text=col)
    staff_table.column(col, anchor="center", width=80)
staff_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
show_staff(staff_table)
window.mainloop()
