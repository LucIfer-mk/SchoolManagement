import mysql.connector

conn = mysql.connector.connect(
host = "localhost",
user = "root",
password = "mkkapri"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS studentManagement")
# print("data base is there")

cursor.execute("USE studentManagement")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);
""")
# Student Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(100),
    year INT,
    department VARCHAR(50) DEFAULT 'IT',
    address VARCHAR(100),
    dob DATE,
    gender VARCHAR(10)
);
""")

# Staff Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    designation VARCHAR(100),
    department VARCHAR(50) DEFAULT 'IT',
    phone VARCHAR(20)
);
""")

# Student Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    date DATE,
    status VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
        ON DELETE CASCADE
);
""")

# Staff Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff_attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT,
    date DATE,
    status VARCHAR(10),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
        ON DELETE CASCADE
);
""")

# Subject Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    year INT,
    department VARCHAR(50) DEFAULT 'IT'
);
""")

# Student Result Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    marks FLOAT,
    max_marks FLOAT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
        ON DELETE CASCADE
);
""")

# print("Table Created Sucessfully")

cursor.close()
conn.close()

# ALTER TABLE staff_attendance ADD UNIQUE KEY unique_staff_date(staff_id, date);
# ALTER TABLE student_attendance ADD UNIQUE KEY unique_student_date(student_id, date);
