
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from services.student_service import StudentService

class StudentsView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="👨‍🎓 Student Enrollment",
            font=("Segoe UI", 26, "bold")
        ).pack(side=LEFT)

        # FORM CONTAINER
        form_container = ttk.Frame(self, bootstyle="dark", padding=20)
        form_container.pack(fill=X, pady=(0, 25))

        ttk.Label(
            form_container,
            text="Student Details",
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark"
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        self.id_var = ttk.StringVar()
        
        # ROW 1: ID & Name
        ttk.Label(form_container, text="Student ID", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.student_id_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.student_id_entry.grid(row=2, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Full Name", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=1, sticky=W)
        self.name_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=40)
        self.name_entry.grid(row=2, column=1, sticky=W, pady=(5, 15), ipady=5)

        # ROW 2: Email & Date
        ttk.Label(form_container, text="Email Address", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=0, sticky=W, padx=(0, 10))
        self.email_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.email_entry.grid(row=4, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Enroll Date (YYYY-MM-DD)", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=1, sticky=W)
        self.date_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=40)
        self.date_entry.grid(row=4, column=1, sticky=W, pady=(5, 15), ipady=5)

        # ACTION BUTTONS
        btn_frame = ttk.Frame(form_container, bootstyle="dark")
        btn_frame.grid(row=5, column=0, columnspan=2, sticky=W, pady=(10, 0))

        ttk.Button(btn_frame, text="💾 Save Student", bootstyle="success", command=self.save_student).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🔄 Clear Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", bootstyle="danger", command=self.delete_student).pack(side=LEFT, ipady=4)

        # DATA TABLE
        table_container = ttk.Frame(self)
        table_container.pack(fill=BOTH, expand=YES)

        columns = ("id", "student_id", "name", "email", "enrollment_date")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle="info"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("email", text="Email Address")
        self.tree.heading("enrollment_date", text="Enrolled")

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("student_id", width=120)
        self.tree.column("name", width=250)
        self.tree.column("email", width=250)
        self.tree.column("enrollment_date", width=150, anchor=CENTER)

        scrollbar = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        students = StudentService.get_all_students()
        for student in students:
            self.tree.insert("", END, values=(student['id'], student['student_id'], student['name'], student['email'], student['enrollment_date']))
        
        self.clear_form()

    def clear_form(self):
        self.id_var.set("")
        self.student_id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.date_entry.delete(0, END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.id_var.set(values[0])
            self.student_id_entry.insert(0, values[1])
            self.name_entry.insert(0, values[2])
            self.email_entry.insert(0, values[3] if values[3] != 'None' else "")
            self.date_entry.insert(0, values[4] if values[4] != 'None' else "")

    def save_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        enroll_date = self.date_entry.get().strip()
        db_id = self.id_var.get()

        if not student_id or not name or not enroll_date:
            Messagebox.show_error("Student ID, Name, and Date are required fields.", "Validation Error")
            return

        if db_id:
            success, msg = StudentService.update_student(db_id, student_id, name, email, enroll_date)
        else:
            success, msg = StudentService.add_student(student_id, name, email, enroll_date)

        if success:
            Messagebox.show_info(msg, "Success")
            self.refresh()
        else:
            Messagebox.show_error(msg, "Database Error")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select a student to delete from the list below.", "No Selection")
            return
            
        if Messagebox.yesno("Are you sure you want to permanently remove this student?", "Confirm Deletion") == "Yes":
            db_id = self.tree.item(selected[0], "values")[0]
            success, msg = StudentService.delete_student(db_id)
            if success:
                self.refresh()
            else:
                Messagebox.show_error(msg, "Deletion Error")
