import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from services.grade_service import GradeService

class GradesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="📊 Grades Tracking",
            font=("Segoe UI", 26, "bold")
        ).pack(side=LEFT)

        # FORM CONTAINER
        form_container = ttk.Frame(self, bootstyle="dark", padding=20)
        form_container.pack(fill=X, pady=(0, 25))

        ttk.Label(
            form_container,
            text="Grade Details",
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark"
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        self.id_var = ttk.StringVar()
        
        # ROW 1: Student & Assignment
        ttk.Label(form_container, text="Student Name/ID", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.student_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=30)
        self.student_entry.grid(row=2, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Assignment", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=1, sticky=W)
        self.assignment_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=30)
        self.assignment_entry.grid(row=2, column=1, sticky=W, pady=(5, 15), ipady=5)

        # ROW 2: Score
        ttk.Label(form_container, text="Score (%)", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=0, sticky=W, padx=(0, 10))
        self.score_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=15)
        self.score_entry.grid(row=4, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        # ACTION BUTTONS
        btn_frame = ttk.Frame(form_container, bootstyle="dark")
        btn_frame.grid(row=5, column=0, columnspan=2, sticky=W, pady=(10, 0))

        ttk.Button(btn_frame, text="💾 Save Grade", bootstyle="success", command=self.save_grade).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🔄 Clear Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", bootstyle="danger", command=self.delete_grade).pack(side=LEFT, ipady=4)

        # DATA TABLE
        table_container = ttk.Frame(self)
        table_container.pack(fill=BOTH, expand=YES)

        columns = ("id", "student", "assignment", "score")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle="success"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("student", text="Student")
        self.tree.heading("assignment", text="Assignment")
        self.tree.heading("score", text="Score")

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("student", width=250)
        self.tree.column("assignment", width=250)
        self.tree.column("score", width=100, anchor=E)

        scrollbar = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        grades = GradeService.get_all_grades()
        for g in grades:
            self.tree.insert("", END, values=(g['id'], g['student'], g['assignment'], g['score']))
        
        self.clear_form()

    def clear_form(self):
        self.id_var.set("")
        self.student_entry.delete(0, END)
        self.assignment_entry.delete(0, END)
        self.score_entry.delete(0, END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.id_var.set(values[0])
            self.student_entry.insert(0, values[1])
            self.assignment_entry.insert(0, values[2])
            self.score_entry.insert(0, values[3])

    def save_grade(self):
        student = self.student_entry.get().strip()
        assignment = self.assignment_entry.get().strip()
        score = self.score_entry.get().strip()
        db_id = self.id_var.get()

        if not student or not assignment or not score:
            Messagebox.show_error("Student, Assignment, and Score are required.", "Validation Error")
            return

        if db_id:
            success, msg = GradeService.update_grade(db_id, student, assignment, score)
        else:
            success, msg = GradeService.add_grade(student, assignment, score)

        if success:
            self.refresh()
        else:
            Messagebox.show_error(msg, "Error")

    def delete_grade(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select a grade entry to delete.", "No Selection")
            return
            
        if Messagebox.yesno("Are you sure you want to delete this grade?", "Confirm Deletion") == "Yes":
            db_id = self.tree.item(selected[0], "values")[0]
            success, msg = GradeService.delete_grade(db_id)
            if success:
                self.refresh()
            else:
                Messagebox.show_error(msg, "Error")
