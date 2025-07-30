import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import mysql.connector
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StudentManagementSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("IT Department Management System")
        self.window.state("zoomed")
        self.window.configure(bg="#f0f2f5")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'accent': '#9b59b6'
        }
        
        self.setup_database()
        self.create_header()
        self.create_notebook()
        self.create_tabs()
        
    def setup_database(self):
        """Initialize database connection"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mkkapri",
                database="studentManagement"
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    
    def create_header(self):
        """Create modern header with gradient effect"""
        header_frame = tk.Frame(self.window, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True, fill='both')
        
        tk.Label(title_frame, text="🎓", font=("Segoe UI", 24), 
                bg=self.colors['primary'], fg=self.colors['white']).pack(side='left', padx=(30, 10), pady=20)
        
        tk.Label(title_frame, text="IT Department Management System", 
                font=("Segoe UI", 24, "bold"), bg=self.colors['primary'], 
                fg=self.colors['white']).pack(side='left', pady=20)
        
        # Current date/time
        datetime_label = tk.Label(title_frame, text=datetime.datetime.now().strftime("%B %d, %Y"), 
                                 font=("Segoe UI", 12), bg=self.colors['primary'], 
                                 fg=self.colors['light'])
        datetime_label.pack(side='right', padx=(10, 30), pady=20)
    
    def create_notebook(self):
        """Create modern styled notebook"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['light'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 11, 'bold'))
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
    
    def create_tabs(self):
        """Create all tabs"""
        # Student tabs
        self.create_student_tabs()
        # Attendance tab
        self.create_attendance_tab()
        # Staff tab
        self.create_staff_tab()
        # Dashboard tab
        self.create_dashboard_tab()
    
    def create_student_tabs(self):
        """Create student management tabs"""
        for year in [1, 2, 3]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f'{year}{"st" if year==1 else "nd" if year==2 else "rd"} Year Students')
            self.setup_student_tab(frame, year)
    
    def setup_student_tab(self, parent, year):
        """Setup individual student tab with modern UI"""
        # Main container
        container = tk.Frame(parent, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        header = tk.Frame(container, bg=self.colors['white'], height=60)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        # Title and stats
        tk.Label(header, text=f"{year}{'st' if year==1 else 'nd' if year==2 else 'rd'} Year Students", 
                font=("Segoe UI", 18, "bold"), bg=self.colors['white'], 
                fg=self.colors['dark']).pack(side='left', pady=15)
        
        # Modern buttons
        btn_frame = tk.Frame(header, bg=self.colors['white'])
        btn_frame.pack(side='right', pady=15)
        
        add_btn = tk.Button(btn_frame, text="➕ Add Student", 
                           command=lambda: self.add_student_dialog(),
                           font=("Segoe UI", 10, "bold"), bg=self.colors['success'], 
                           fg=self.colors['white'], relief='flat', padx=20, pady=8,
                           cursor='hand2')
        add_btn.pack(side='right', padx=(10, 0))
        
        refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", 
                               command=lambda: self.load_students_by_year(year, getattr(self, f'student_tree_{year}')),
                               font=("Segoe UI", 10, "bold"), bg=self.colors['secondary'], 
                               fg=self.colors['white'], relief='flat', padx=20, pady=8,
                               cursor='hand2')
        refresh_btn.pack(side='right', padx=(10, 0))
        
        # Search frame
        search_frame = tk.Frame(container, bg=self.colors['white'])
        search_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 10), 
                bg=self.colors['white']).pack(side='left')
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=30, relief='flat', bd=5)
        search_entry.pack(side='left', padx=(10, 0))
        
        # Student table with modern styling
        table_frame = tk.Frame(container, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True)
        
        # Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side='right', fill='y')
        
        columns = ("ID", "Roll No", "Name", "Email", "Contact", "Status", "Actions")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                           yscrollcommand=tree_scroll.set, height=15)
        
        # Configure columns
        tree.heading("ID", text="Student ID")
        tree.heading("Roll No", text="Roll Number")
        tree.heading("Name", text="Full Name")
        tree.heading("Email", text="Email Address")
        tree.heading("Contact", text="Contact")
        tree.heading("Status", text="Status")
        tree.heading("Actions", text="Actions")
        
        # Column widths
        tree.column("ID", width=80, anchor='center')
        tree.column("Roll No", width=100, anchor='center')
        tree.column("Name", width=150)
        tree.column("Email", width=180)
        tree.column("Contact", width=120)
        tree.column("Status", width=80, anchor='center')
        tree.column("Actions", width=100, anchor='center')
        
        tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=tree.yview)
        
        # Bind double-click event
        tree.bind("<Double-1>", lambda e: self.show_student_details(tree, year))
        
        # Store tree reference
        setattr(self, f'student_tree_{year}', tree)
        
        # Load initial data
        self.load_students_by_year(year, tree)
    
    def add_student_dialog(self):
        """Modern add student dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Add New Student")
        dialog.geometry("800x800")
        dialog.configure(bg=self.colors['white'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Add New Student", font=("Segoe UI", 16, "bold"),
                bg=self.colors['primary'], fg=self.colors['white']).pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(dialog, bg=self.colors['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Form fields
        fields = {}
        
        # Roll Number
        tk.Label(form_frame, text="Roll Number *", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=0, column=0, sticky='w', pady=(0, 5))
        fields['roll_number'] = tk.Entry(form_frame, font=("Segoe UI", 10), width=35, relief='solid', bd=1)
        fields['roll_number'].grid(row=1, column=0, pady=(0, 15), ipady=5)
        
        # Name
        tk.Label(form_frame, text="Full Name *", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=2, column=0, sticky='w', pady=(0, 5))
        fields['name'] = tk.Entry(form_frame, font=("Segoe UI", 10), width=35, relief='solid', bd=1)
        fields['name'].grid(row=3, column=0, pady=(0, 15), ipady=5)
        
        # Email
        tk.Label(form_frame, text="Email Address", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=4, column=0, sticky='w', pady=(0, 5))
        fields['email'] = tk.Entry(form_frame, font=("Segoe UI", 10), width=35, relief='solid', bd=1)
        fields['email'].grid(row=5, column=0, pady=(0, 15), ipady=5)
        
        # Contact
        tk.Label(form_frame, text="Contact Number", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=6, column=0, sticky='w', pady=(0, 5))
        fields['contact'] = tk.Entry(form_frame, font=("Segoe UI", 10), width=35, relief='solid', bd=1)
        fields['contact'].grid(row=7, column=0, pady=(0, 15), ipady=5)
        
        # Address
        tk.Label(form_frame, text="Address", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=8, column=0, sticky='w', pady=(0, 5))
        fields['address'] = tk.Text(form_frame, font=("Segoe UI", 10), width=35, height=3, relief='solid', bd=1)
        fields['address'].grid(row=9, column=0, pady=(0, 15))
        
        # Gender
        tk.Label(form_frame, text="Gender *", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=10, column=0, sticky='w', pady=(0, 5))
        gender_frame = tk.Frame(form_frame, bg=self.colors['white'])
        gender_frame.grid(row=11, column=0, sticky='w', pady=(0, 15))
        
        fields['gender'] = tk.StringVar(value="Male")
        tk.Radiobutton(gender_frame, text="Male", variable=fields['gender'], value="Male",
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left')
        tk.Radiobutton(gender_frame, text="Female", variable=fields['gender'], value="Female",
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left', padx=(20, 0))
        tk.Radiobutton(gender_frame, text="Other", variable=fields['gender'], value="Other",
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left', padx=(20, 0))
        
        # Year
        tk.Label(form_frame, text="Academic Year *", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=12, column=0, sticky='w', pady=(0, 5))
        year_frame = tk.Frame(form_frame, bg=self.colors['white'])
        year_frame.grid(row=13, column=0, sticky='w', pady=(0, 15))
        
        fields['year'] = tk.IntVar(value=1)
        tk.Radiobutton(year_frame, text="1st Year", variable=fields['year'], value=1,
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left')
        tk.Radiobutton(year_frame, text="2nd Year", variable=fields['year'], value=2,
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left', padx=(20, 0))
        tk.Radiobutton(year_frame, text="3rd Year", variable=fields['year'], value=3,
                      bg=self.colors['white'], font=("Segoe UI", 10)).pack(side='left', padx=(20, 0))
        
        # Date of Birth
        tk.Label(form_frame, text="Date of Birth", font=("Segoe UI", 10, "bold"),
                bg=self.colors['white']).grid(row=14, column=0, sticky='w', pady=(0, 5))
        fields['dob'] = DateEntry(form_frame, width=32, background='darkblue',
                                 foreground='white', borderwidth=2, year=2000)
        fields['dob'].grid(row=15, column=0, pady=(0, 20), ipady=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['white'])
        btn_frame.grid(row=16, column=0, pady=20)
        
        def save_student():
            # Validation
            if not fields['roll_number'].get() or not fields['name'].get():
                messagebox.showerror("Validation Error", "Roll Number and Name are required!")
                return
            
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO student (roll_number, name, email, contact, address, gender, year, dob)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    fields['roll_number'].get(),
                    fields['name'].get(),
                    fields['email'].get() or None,
                    fields['contact'].get() or None,
                    fields['address'].get('1.0', 'end-1c') or None,
                    fields['gender'].get(),
                    fields['year'].get(),
                    fields['dob'].get_date()
                ))
                self.conn.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                
                # Refresh the appropriate table
                year = fields['year'].get()
                if hasattr(self, f'student_tree_{year}'):
                    self.load_students_by_year(year, getattr(self, f'student_tree_{year}'))
                    
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Failed to add student: {e}")
        
        tk.Button(btn_frame, text="💾 Save Student", command=save_student,
                 font=("Segoe UI", 11, "bold"), bg=self.colors['success'], 
                 fg=self.colors['white'], relief='flat', padx=20, pady=10,
                 cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=("Segoe UI", 11, "bold"), bg=self.colors['danger'], 
                 fg=self.colors['white'], relief='flat', padx=20, pady=10,
                 cursor='hand2').pack(side='left')
    
    def load_students_by_year(self, year, tree):
        """Load students with enhanced data"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT s.student_id, s.roll_number, s.name, s.email, s.contact, s.status
                FROM student s 
                WHERE s.year = %s AND s.status = 'Active'
                ORDER BY s.roll_number
            """, (year,))
            records = cursor.fetchall()
            
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Insert new data
            for row in records:
                tree.insert('', 'end', values=(*row, "View Details"))
            
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load students: {e}")
    
    def show_student_details(self, tree, year):
        """Show detailed student information with analytics"""
        selection = tree.selection()
        if not selection:
            return
        
        student_data = tree.item(selection[0], 'values')
        student_id = student_data[0]
        
        # Create detail window
        detail_window = tk.Toplevel(self.window)
        detail_window.title(f"Student Details - {student_data[2]}")
        detail_window.geometry("900x700")
        detail_window.configure(bg=self.colors['light'])
        
        # Create notebook for different sections
        detail_notebook = ttk.Notebook(detail_window)
        detail_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Personal Info Tab
        self.create_personal_info_tab(detail_notebook, student_id)
        
        # Attendance Tab
        self.create_student_attendance_tab(detail_notebook, student_id)
        
        # Results Tab
        self.create_student_results_tab(detail_notebook, student_id)
        
        # Analytics Tab
        self.create_student_analytics_tab(detail_notebook, student_id)
    
    def create_personal_info_tab(self, notebook, student_id):
        """Create personal information tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📋 Personal Info")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT roll_number, name, email, contact, address, gender, year, dob, 
                       admission_date, status, created_at
                FROM student WHERE student_id = %s
            """, (student_id,))
            student = cursor.fetchone()
            cursor.close()
            
            if student:
                # Create info display
                info_frame = tk.Frame(frame, bg=self.colors['white'])
                info_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Profile header
                header = tk.Frame(info_frame, bg=self.colors['primary'], height=100)
                header.pack(fill='x', pady=(0, 20))
                header.pack_propagate(False)
                
                tk.Label(header, text="👤", font=("Segoe UI", 30),
                        bg=self.colors['primary'], fg=self.colors['white']).pack(side='left', padx=30, pady=20)
                
                name_frame = tk.Frame(header, bg=self.colors['primary'])
                name_frame.pack(side='left', pady=20)
                
                tk.Label(name_frame, text=student[1], font=("Segoe UI", 18, "bold"),
                        bg=self.colors['primary'], fg=self.colors['white']).pack(anchor='w')
                tk.Label(name_frame, text=f"Roll No: {student[0]}", font=("Segoe UI", 12),
                        bg=self.colors['primary'], fg=self.colors['light']).pack(anchor='w')
                
                # Information grid
                info_grid = tk.Frame(info_frame, bg=self.colors['white'])
                info_grid.pack(fill='both', expand=True)
                
                labels = [
                    ("Email:", student[2] or "Not provided"),
                    ("Contact:", student[3] or "Not provided"),
                    ("Address:", student[4] or "Not provided"),
                    ("Gender:", student[5]),
                    ("Year:", f"{student[6]} {'Year' if student[6] else ''}"),
                    ("Date of Birth:", str(student[7]) if student[7] else "Not provided"),
                    ("Admission Date:", str(student[8]) if student[8] else "Not provided"),
                    ("Status:", student[9]),
                    ("Registered On:", str(student[10])[:10] if student[10] else "Unknown")
                ]
                
                for i, (label, value) in enumerate(labels):
                    row = i // 2
                    col = (i % 2) * 2
                    
                    tk.Label(info_grid, text=label, font=("Segoe UI", 11, "bold"),
                            bg=self.colors['white'], fg=self.colors['dark']).grid(
                            row=row, column=col, sticky='w', padx=20, pady=10)
                    
                    tk.Label(info_grid, text=str(value), font=("Segoe UI", 11),
                            bg=self.colors['white'], fg=self.colors['primary']).grid(
                            row=row, column=col+1, sticky='w', padx=20, pady=10)
                
        except mysql.connector.Error as e:
            tk.Label(frame, text=f"Error loading student data: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def create_student_attendance_tab(self, notebook, student_id):
        """Create student attendance analysis tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📊 Attendance")
        
        try:
            cursor = self.conn.cursor()
            
            # Get attendance summary
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_days,
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_days,
                    SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
                    SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late_days
                FROM student_attendance 
                WHERE student_id = %s
            """, (student_id,))
            
            attendance_summary = cursor.fetchone()
            
            # Get monthly attendance
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(date, '%Y-%m') as month,
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
                FROM student_attendance 
                WHERE student_id = %s
                GROUP BY DATE_FORMAT(date, '%Y-%m')
                ORDER BY month DESC
                LIMIT 6
            """, (student_id,))
            
            monthly_data = cursor.fetchall()
            cursor.close()
            
            # Create attendance dashboard
            dashboard = tk.Frame(frame, bg=self.colors['white'])
            dashboard.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Summary cards
            summary_frame = tk.Frame(dashboard, bg=self.colors['white'])
            summary_frame.pack(fill='x', pady=(0, 20))
            
            if attendance_summary and attendance_summary[0] > 0:
                total_days = attendance_summary[0]
                present_days = attendance_summary[1] or 0
                absent_days = attendance_summary[2] or 0
                late_days = attendance_summary[3] or 0
                attendance_percentage = (present_days / total_days) * 100 if total_days > 0 else 0
                
                cards_data = [
                    ("Total Days", total_days, self.colors['primary']),
                    ("Present", present_days, self.colors['success']),
                    ("Absent", absent_days, self.colors['danger']),
                    ("Attendance %", f"{attendance_percentage:.1f}%", self.colors['accent'])
                ]
                
                for i, (title, value, color) in enumerate(cards_data):
                    card = tk.Frame(summary_frame, bg=color, relief='flat', bd=0)
                    card.pack(side='left', padx=10, pady=10, fill='both', expand=True)
                    
                    tk.Label(card, text=str(value), font=("Segoe UI", 20, "bold"),
                            bg=color, fg=self.colors['white']).pack(pady=(15, 5))
                    tk.Label(card, text=title, font=("Segoe UI", 12),
                            bg=color, fg=self.colors['white']).pack(pady=(0, 15))
            else:
                tk.Label(summary_frame, text="No attendance records found",
                        font=("Segoe UI", 14), fg=self.colors['danger']).pack(pady=50)
            
            # Monthly trend chart
            if monthly_data:
                chart_frame = tk.Frame(dashboard, bg=self.colors['white'])
                chart_frame.pack(fill='both', expand=True, pady=20)
                
                tk.Label(chart_frame, text="Monthly Attendance Trend", 
                        font=("Segoe UI", 14, "bold"), bg=self.colors['white']).pack(pady=(0, 10))
                
                # Create matplotlib chart
                fig = Figure(figsize=(8, 4), dpi=100, facecolor='white')
                ax = fig.add_subplot(111)
                
                months = [data[0] for data in monthly_data]
                percentages = [(data[2]/data[1])*100 if data[1] > 0 else 0 for data in monthly_data]
                
                ax.plot(months, percentages, marker='o', linewidth=2, color=self.colors['secondary'])
                ax.set_title('Monthly Attendance Percentage', fontsize=12, fontweight='bold')
                ax.set_ylabel('Attendance %')
                ax.set_ylim(0, 100)
                ax.grid(True, alpha=0.3)
                
                canvas = FigureCanvasTkAgg(fig, chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
        except mysql.connector.Error as e:
            tk.Label(frame, text=f"Error loading attendance data: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def create_student_results_tab(self, notebook, student_id):
        """Create student results analysis tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📈 Results")
        
        try:
            cursor = self.conn.cursor()
            
            # Get results summary
            cursor.execute("""
                SELECT 
                    s.name as subject_name,
                    sr.exam_type,
                    sr.marks,
                    sr.max_marks,
                    sr.grade,
                    sr.exam_date,
                    (sr.marks/sr.max_marks)*100 as percentage
                FROM student_result sr
                JOIN subject s ON sr.subject_id = s.subject_id
                WHERE sr.student_id = %s
                ORDER BY sr.exam_date DESC
            """, (student_id,))
            
            results = cursor.fetchall()
            
            # Get overall statistics
            cursor.execute("""
                SELECT 
                    AVG((marks/max_marks)*100) as avg_percentage,
                    MAX((marks/max_marks)*100) as max_percentage,
                    MIN((marks/max_marks)*100) as min_percentage,
                    COUNT(*) as total_exams
                FROM student_result 
                WHERE student_id = %s
            """, (student_id,))
            
            stats = cursor.fetchone()
            cursor.close()
            
            # Create results dashboard
            results_container = tk.Frame(frame, bg=self.colors['white'])
            results_container.pack(fill='both', expand=True, padx=20, pady=20)
            
            if results:
                # Statistics cards
                stats_frame = tk.Frame(results_container, bg=self.colors['white'])
                stats_frame.pack(fill='x', pady=(0, 20))
                
                if stats and stats[3] > 0:  # total_exams > 0
                    stats_cards = [
                        ("Average", f"{stats[0]:.1f}%", self.colors['primary']),
                        ("Highest", f"{stats[1]:.1f}%", self.colors['success']),
                        ("Lowest", f"{stats[2]:.1f}%", self.colors['warning']),
                        ("Total Exams", stats[3], self.colors['accent'])
                    ]
                    
                    for title, value, color in stats_cards:
                        card = tk.Frame(stats_frame, bg=color, relief='flat')
                        card.pack(side='left', padx=10, fill='both', expand=True)
                        
                        tk.Label(card, text=str(value), font=("Segoe UI", 16, "bold"),
                                bg=color, fg=self.colors['white']).pack(pady=(10, 5))
                        tk.Label(card, text=title, font=("Segoe UI", 10),
                                bg=color, fg=self.colors['white']).pack(pady=(0, 10))
                
                # Results table
                table_frame = tk.Frame(results_container, bg=self.colors['white'])
                table_frame.pack(fill='both', expand=True)
                
                tk.Label(table_frame, text="Detailed Results", font=("Segoe UI", 14, "bold"),
                        bg=self.colors['white']).pack(pady=(0, 10))
                
                # Treeview for results
                columns = ("Subject", "Exam Type", "Marks", "Max Marks", "Percentage", "Grade", "Date")
                results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
                
                for col in columns:
                    results_tree.heading(col, text=col)
                    results_tree.column(col, width=100, anchor='center')
                
                # Insert data
                for result in results:
                    percentage = f"{result[6]:.1f}%" if result[6] else "N/A"
                    results_tree.insert('', 'end', values=(
                        result[0], result[1], result[2], result[3], 
                        percentage, result[4] or "N/A", str(result[5]) if result[5] else "N/A"
                    ))
                
                results_tree.pack(fill='both', expand=True)
                
                # Scrollbar for results table
                scrollbar_results = ttk.Scrollbar(table_frame, orient="vertical", command=results_tree.yview)
                scrollbar_results.pack(side='right', fill='y')
                results_tree.configure(yscrollcommand=scrollbar_results.set)
                
            else:
                tk.Label(results_container, text="No results found for this student",
                        font=("Segoe UI", 14), fg=self.colors['danger']).pack(pady=50)
                
        except mysql.connector.Error as e:
            tk.Label(frame, text=f"Error loading results data: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def create_student_analytics_tab(self, notebook, student_id):
        """Create student analytics tab with charts"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📊 Analytics")
        
        analytics_container = tk.Frame(frame, bg=self.colors['white'])
        analytics_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        try:
            cursor = self.conn.cursor()
            
            # Get performance trend data
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(exam_date, '%Y-%m') as month,
                    AVG((marks/max_marks)*100) as avg_percentage
                FROM student_result 
                WHERE student_id = %s AND exam_date IS NOT NULL
                GROUP BY DATE_FORMAT(exam_date, '%Y-%m')
                ORDER BY month
            """, (student_id,))
            
            performance_trend = cursor.fetchall()
            
            # Get subject-wise performance
            cursor.execute("""
                SELECT 
                    s.name as subject,
                    AVG((sr.marks/sr.max_marks)*100) as avg_percentage
                FROM student_result sr
                JOIN subject s ON sr.subject_id = s.subject_id
                WHERE sr.student_id = %s
                GROUP BY s.subject_id, s.name
                ORDER BY avg_percentage DESC
            """, (student_id,))
            
            subject_performance = cursor.fetchall()
            cursor.close()
            
            # Create charts
            if performance_trend or subject_performance:
                chart_container = tk.Frame(analytics_container, bg=self.colors['white'])
                chart_container.pack(fill='both', expand=True)
                
                # Performance trend chart
                if performance_trend:
                    trend_frame = tk.Frame(chart_container, bg=self.colors['white'])
                    trend_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
                    
                    tk.Label(trend_frame, text="Performance Trend", 
                            font=("Segoe UI", 12, "bold"), bg=self.colors['white']).pack(pady=(0, 10))
                    
                    fig1 = Figure(figsize=(6, 4), dpi=100, facecolor='white')
                    ax1 = fig1.add_subplot(111)
                    
                    months = [data[0] for data in performance_trend]
                    percentages = [data[1] for data in performance_trend]
                    
                    ax1.plot(months, percentages, marker='o', linewidth=2, color=self.colors['secondary'])
                    ax1.set_title('Academic Performance Over Time')
                    ax1.set_ylabel('Average Percentage')
                    ax1.grid(True, alpha=0.3)
                    
                    canvas1 = FigureCanvasTkAgg(fig1, trend_frame)
                    canvas1.draw()
                    canvas1.get_tk_widget().pack(fill='both', expand=True)
                
                # Subject performance chart
                if subject_performance:
                    subject_frame = tk.Frame(chart_container, bg=self.colors['white'])
                    subject_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
                    
                    tk.Label(subject_frame, text="Subject-wise Performance", 
                            font=("Segoe UI", 12, "bold"), bg=self.colors['white']).pack(pady=(0, 10))
                    
                    fig2 = Figure(figsize=(6, 4), dpi=100, facecolor='white')
                    ax2 = fig2.add_subplot(111)
                    
                    subjects = [data[0][:10] + "..." if len(data[0]) > 10 else data[0] for data in subject_performance]
                    scores = [data[1] for data in subject_performance]
                    
                    bars = ax2.bar(subjects, scores, color=self.colors['accent'], alpha=0.7)
                    ax2.set_title('Subject Performance Comparison')
                    ax2.set_ylabel('Average Percentage')
                    ax2.set_ylim(0, 100)
                    
                    # Rotate x-axis labels for better readability
                    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
                    
                    canvas2 = FigureCanvasTkAgg(fig2, subject_frame)
                    canvas2.draw()
                    canvas2.get_tk_widget().pack(fill='both', expand=True)
            
            else:
                tk.Label(analytics_container, text="Insufficient data for analytics",
                        font=("Segoe UI", 14), fg=self.colors['warning']).pack(pady=50)
                
        except mysql.connector.Error as e:
            tk.Label(analytics_container, text=f"Error loading analytics data: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def create_attendance_tab(self):
        """Create attendance management tab"""
        attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(attendance_frame, text="📅 Attendance")
        
        # Create sub-notebook for different years
        attendance_notebook = ttk.Notebook(attendance_frame)
        attendance_notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        for year in [1, 2, 3]:
            year_frame = ttk.Frame(attendance_notebook)
            attendance_notebook.add(year_frame, text=f"{year}{'st' if year==1 else 'nd' if year==2 else 'rd'} Year")
            self.create_attendance_year_tab(year_frame, year)
    
    def create_attendance_year_tab(self, parent, year):
        """Create attendance tab for specific year"""
        container = tk.Frame(parent, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        tk.Label(container, text=f"{year}{'st' if year==1 else 'nd' if year==2 else 'rd'} Year Attendance Management", 
                font=("Segoe UI", 16, "bold"), bg=self.colors['white']).pack(pady=(0, 20))
        
        # Date selection
        date_frame = tk.Frame(container, bg=self.colors['white'])
        date_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(date_frame, text="Select Date:", font=("Segoe UI", 12, "bold"),
                bg=self.colors['white']).pack(side='left', padx=(0, 10))
        
        date_entry = DateEntry(date_frame, width=12, background=self.colors['primary'],
                              foreground='white', borderwidth=2, year=2025)
        date_entry.pack(side='left')
        
        # Load attendance button
        load_btn = tk.Button(date_frame, text="📋 Load Students", 
                           command=lambda: self.load_attendance_students(year, date_entry.get_date(), attendance_frame),
                           font=("Segoe UI", 10, "bold"), bg=self.colors['secondary'], 
                           fg=self.colors['white'], relief='flat', padx=15, pady=5)
        load_btn.pack(side='left', padx=(20, 0))
        
        # Attendance frame
        attendance_frame = tk.Frame(container, bg=self.colors['white'])
        attendance_frame.pack(fill='both', expand=True)
        
        # Initial load
        self.load_attendance_students(year, date_entry.get_date(), attendance_frame)
    
    def load_attendance_students(self, year, date, parent_frame):
        """Load students for attendance marking"""
        # Clear previous content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT student_id, roll_number, name 
                FROM student 
                WHERE year = %s AND status = 'Active'
                ORDER BY roll_number
            """, (year,))
            
            students = cursor.fetchall()
            
            if students:
                # Create scrollable frame
                canvas = tk.Canvas(parent_frame, bg=self.colors['white'])
                scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Header
                header_frame = tk.Frame(scrollable_frame, bg=self.colors['light'])
                header_frame.pack(fill='x', pady=(0, 10))
                
                tk.Label(header_frame, text="Roll No", font=("Segoe UI", 11, "bold"),
                        bg=self.colors['light'], width=15).pack(side='left', padx=10, pady=10)
                tk.Label(header_frame, text="Student Name", font=("Segoe UI", 11, "bold"),
                        bg=self.colors['light'], width=30).pack(side='left', padx=10, pady=10)
                tk.Label(header_frame, text="Attendance Status", font=("Segoe UI", 11, "bold"),
                        bg=self.colors['light']).pack(side='left', padx=10, pady=10)
                
                # Student attendance rows
                attendance_vars = []
                
                for student in students:
                    student_id, roll_no, name = student
                    
                    row_frame = tk.Frame(scrollable_frame, bg=self.colors['white'], relief='solid', bd=1)
                    row_frame.pack(fill='x', pady=2)
                    
                    tk.Label(row_frame, text=roll_no, font=("Segoe UI", 10),
                            bg=self.colors['white'], width=15).pack(side='left', padx=10, pady=5)
                    tk.Label(row_frame, text=name, font=("Segoe UI", 10),
                            bg=self.colors['white'], width=30, anchor='w').pack(side='left', padx=10, pady=5)
                    
                    # Attendance options
                    attendance_var = tk.StringVar(value="Present")
                    attendance_vars.append((student_id, attendance_var))
                    
                    status_frame = tk.Frame(row_frame, bg=self.colors['white'])
                    status_frame.pack(side='left', padx=10, pady=5)
                    
                    tk.Radiobutton(status_frame, text="Present", variable=attendance_var, value="Present",
                                  bg=self.colors['white'], font=("Segoe UI", 9)).pack(side='left')
                    tk.Radiobutton(status_frame, text="Absent", variable=attendance_var, value="Absent",
                                  bg=self.colors['white'], font=("Segoe UI", 9)).pack(side='left', padx=(10, 0))
                    tk.Radiobutton(status_frame, text="Late", variable=attendance_var, value="Late",
                                  bg=self.colors['white'], font=("Segoe UI", 9)).pack(side='left', padx=(10, 0))
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Submit button
                submit_frame = tk.Frame(parent_frame, bg=self.colors['white'])
                submit_frame.pack(fill='x', pady=20)
                
                def submit_attendance():
                    try:
                        cursor = self.conn.cursor()
                        for student_id, var in attendance_vars:
                            cursor.execute("""
                                INSERT INTO student_attendance (student_id, date, status)
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE status = %s
                            """, (student_id, date, var.get(), var.get()))
                        
                        self.conn.commit()
                        cursor.close()
                        messagebox.showinfo("Success", f"Attendance saved for {len(attendance_vars)} students!")
                        
                    except mysql.connector.Error as e:
                        messagebox.showerror("Database Error", f"Failed to save attendance: {e}")
                
                tk.Button(submit_frame, text="💾 Save Attendance", command=submit_attendance,
                         font=("Segoe UI", 12, "bold"), bg=self.colors['success'], 
                         fg=self.colors['white'], relief='flat', padx=30, pady=10).pack()
            
            else:
                tk.Label(parent_frame, text="No students found for this year",
                        font=("Segoe UI", 14), fg=self.colors['warning']).pack(pady=50)
            
            cursor.close()
            
        except mysql.connector.Error as e:
            tk.Label(parent_frame, text=f"Error loading students: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def create_staff_tab(self):
        """Create staff management tab"""
        staff_frame = ttk.Frame(self.notebook)
        self.notebook.add(staff_frame, text="👥 Staff")
        
        # Similar implementation to students but for staff
        # This would include staff list, add staff, staff details, etc.
        container = tk.Frame(staff_frame, bg=self.colors['white'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(container, bg=self.colors['white'])
        header.pack(fill='x', pady=(0, 20))
        
        tk.Label(header, text="Staff Management", font=("Segoe UI", 18, "bold"),
                bg=self.colors['white']).pack(side='left')
        
        tk.Button(header, text="➕ Add Staff", command=self.add_staff_dialog,
                 font=("Segoe UI", 10, "bold"), bg=self.colors['success'], 
                 fg=self.colors['white'], relief='flat', padx=20, pady=8).pack(side='right')
        
        # Staff table
        columns = ("ID", "Employee ID", "Name", "Email", "Designation", "Phone", "Status")
        self.staff_tree = ttk.Treeview(container, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=120, anchor='center')
        
        self.staff_tree.pack(fill='both', expand=True)
        self.staff_tree.bind("<Double-1>", self.show_staff_details)
        
        # Load staff data
        self.load_staff_data()
    
    def add_staff_dialog(self):
        """Add staff member dialog"""
        # Similar to add_student_dialog but for staff
        pass
    
    def load_staff_data(self):
        """Load staff data into the tree"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT staff_id, employee_id, name, email, designation, phone, status
                FROM staff
                WHERE status = 'Active'
                ORDER BY name
            """)
            
            records = cursor.fetchall()
            
            # Clear existing items
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)
            
            # Insert new data
            for row in records:
                self.staff_tree.insert('', 'end', values=row)
            
            cursor.close()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load staff: {e}")
    
    def show_staff_details(self, event):
        """Show detailed staff information"""
        selection = self.staff_tree.selection()
        if not selection:
            return
        
        staff_data = self.staff_tree.item(selection[0], 'values')
        staff_id = staff_data[0]
        
        # Create staff detail window similar to student details
        messagebox.showinfo("Staff Details", f"Staff detail view for {staff_data[2]} will be implemented here")
    
    def create_dashboard_tab(self):
        """Create dashboard with overall statistics"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        container = tk.Frame(dashboard_frame, bg=self.colors['light'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Dashboard content
        tk.Label(container, text="📊 Department Dashboard", 
                font=("Segoe UI", 20, "bold"), bg=self.colors['light']).pack(pady=20)
        
        # Statistics cards
        stats_frame = tk.Frame(container, bg=self.colors['light'])
        stats_frame.pack(fill='x', pady=20)
        
        try:
            cursor = self.conn.cursor()
            
            # Get various statistics
            queries = [
                ("Total Students", "SELECT COUNT(*) FROM student WHERE status = 'Active'"),
                ("Total Staff", "SELECT COUNT(*) FROM staff WHERE status = 'Active'"),
                ("Today's Attendance", "SELECT COUNT(*) FROM student_attendance WHERE date = CURDATE()"),
                ("Subjects", "SELECT COUNT(*) FROM subject WHERE status = 'Active'")
            ]
            
            for i, (title, query) in enumerate(queries):
                cursor.execute(query)
                count = cursor.fetchone()[0]
                
                card = tk.Frame(stats_frame, bg=self.colors['primary'], relief='flat')
                card.pack(side='left', padx=10, fill='both', expand=True)
                
                tk.Label(card, text=str(count), font=("Segoe UI", 24, "bold"),
                        bg=self.colors['primary'], fg=self.colors['white']).pack(pady=(20, 5))
                tk.Label(card, text=title, font=("Segoe UI", 12),
                        bg=self.colors['primary'], fg=self.colors['white']).pack(pady=(0, 20))
            
            cursor.close()
            
        except mysql.connector.Error as e:
            tk.Label(container, text=f"Error loading dashboard data: {e}",
                    fg=self.colors['danger']).pack(pady=50)
    
    def run(self):
        """Start the application"""
        self.window.mainloop()
        
        # Close database connection when application closes
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

# Run the application
if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()