import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mkkapri"
)

cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS studentManagement")

cursor.execute("USE studentManagement")

# Admin Table
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
    roll_number VARCHAR(20) UNIQUE NOT NULL,  -- Added unique roll number
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,  -- Added email field
    contact VARCHAR(15),
    year INT CHECK (year IN (1, 2, 3)),
    department VARCHAR(50) DEFAULT 'IT',
    address TEXT,  -- Changed to TEXT for longer addresses
    dob DATE,
    gender ENUM('Male', 'Female', 'Other'),  -- Better than VARCHAR
    admission_date DATE DEFAULT (CURRENT_DATE),  -- Track admission
    status ENUM('Active', 'Inactive', 'Graduated') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
""")

# Staff Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) UNIQUE NOT NULL,  -- Added employee ID
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    designation VARCHAR(100),
    department VARCHAR(50) DEFAULT 'IT',
    phone VARCHAR(15),
    salary DECIMAL(10,2),  -- Added salary field
    hire_date DATE,  -- Added hire date
    status ENUM('Active', 'Inactive', 'On Leave') DEFAULT 'Active',
    address TEXT,  -- Added address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
""")

# Subject Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(10) UNIQUE NOT NULL,  -- Added subject code
    name VARCHAR(100) NOT NULL,
    year INT CHECK (year IN (1, 2, 3)),
    department VARCHAR(50) DEFAULT 'IT',
    credits INT DEFAULT 3,  -- Added credit system
    semester INT CHECK (semester IN (1, 2)),  -- Added semester
    staff_id INT,  -- Subject teacher
    description TEXT,
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL
);
""")

# Student Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT,  -- Attendance per subject
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late', 'Excused') DEFAULT 'Present',
    remarks TEXT,  -- Additional notes
    marked_by INT,  -- Which staff marked attendance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES staff(staff_id) ON DELETE SET NULL,
    UNIQUE KEY unique_student_subject_date(student_id, subject_id, date)
);
""")

# Staff Attendance Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff_attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT,
    date DATE,
    status ENUM('Present', 'Absent', 'On Leave') DEFAULT 'Present',  -- Changed to ENUM
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
        ON DELETE CASCADE
);
""")

# Student Result Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    exam_type ENUM('Internal', 'Semester', 'Final', 'Assignment') NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL,
    grade CHAR(2),  -- A+, A, B+, etc.
    exam_date DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id) ON DELETE CASCADE,
    INDEX idx_student_subject (student_id, subject_id)
);
""")

# Academic Year Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS academic_year (
    year_id INT AUTO_INCREMENT PRIMARY KEY,
    year_name VARCHAR(20) UNIQUE NOT NULL,  -- e.g., "2024-25"
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Student Fees Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    academic_year_id INT NOT NULL,
    total_fee DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    due_date DATE,
    payment_status ENUM('Pending', 'Partial', 'Paid', 'Overdue') DEFAULT 'Pending',
    last_payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_year(year_id)
);
""")

# Notifications Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    target_type ENUM('All', 'Students', 'Staff', 'Year') NOT NULL,
    target_year INT,  -- If target_type is 'Year'
    created_by INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES staff(staff_id) ON DELETE SET NULL
);
""")

# System Logs Table (Optional)
cursor.execute("""
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(100),
    performed_by INT,
    user_type ENUM('Admin', 'Staff'),
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Print success message
print("Tables created successfully")

# Close the connection
cursor.close()
conn.close()
