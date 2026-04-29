import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from services.assignment_service import AssignmentService

class AssignmentsView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="📝 Assignment Management",
            font=("Segoe UI", 26, "bold")
        ).pack(side=LEFT)

        # FORM CONTAINER
        form_container = ttk.Frame(self, bootstyle="dark", padding=20)
        form_container.pack(fill=X, pady=(0, 25))

        ttk.Label(
            form_container,
            text="Assignment Details",
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark"
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        self.id_var = ttk.StringVar()
        
        # ROW 1: Course & Title
        ttk.Label(form_container, text="Course Name/Code", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.course_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.course_entry.grid(row=2, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Assignment Title", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=1, sticky=W)
        self.title_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=40)
        self.title_entry.grid(row=2, column=1, sticky=W, pady=(5, 15), ipady=5)

        # ROW 2: Due Date
        ttk.Label(form_container, text="Due Date (YYYY-MM-DD)", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=0, sticky=W, padx=(0, 10))
        self.date_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.date_entry.grid(row=4, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        # ACTION BUTTONS
        btn_frame = ttk.Frame(form_container, bootstyle="dark")
        btn_frame.grid(row=5, column=0, columnspan=2, sticky=W, pady=(10, 0))

        ttk.Button(btn_frame, text="💾 Save Assignment", bootstyle="success", command=self.save_assignment).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🔄 Clear Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", bootstyle="danger", command=self.delete_assignment).pack(side=LEFT, ipady=4)

        # DATA TABLE
        table_container = ttk.Frame(self)
        table_container.pack(fill=BOTH, expand=YES)

        columns = ("id", "course", "title", "due_date")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle="info"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("course", text="Course")
        self.tree.heading("title", text="Assignment Title")
        self.tree.heading("due_date", text="Due Date")

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("course", width=150)
        self.tree.column("title", width=350)
        self.tree.column("due_date", width=150, anchor=CENTER)

        scrollbar = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        assignments = AssignmentService.get_all_assignments()
        for a in assignments:
            self.tree.insert("", END, values=(a['id'], a['course'], a['title'], a['due_date']))
        
        self.clear_form()

    def clear_form(self):
        self.id_var.set("")
        self.course_entry.delete(0, END)
        self.title_entry.delete(0, END)
        self.date_entry.delete(0, END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.id_var.set(values[0])
            self.course_entry.insert(0, values[1])
            self.title_entry.insert(0, values[2])
            self.date_entry.insert(0, values[3])

    def save_assignment(self):
        course = self.course_entry.get().strip()
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        db_id = self.id_var.get()

        if not course or not title or not date:
            Messagebox.show_error("Course, Title, and Date are required fields.", "Validation Error")
            return

        if db_id:
            success, msg = AssignmentService.update_assignment(db_id, course, title, date)
        else:
            success, msg = AssignmentService.add_assignment(course, title, date)

        if success:
            self.refresh()
        else:
            Messagebox.show_error(msg, "Error")

    def delete_assignment(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select an assignment to delete.", "No Selection")
            return
            
        if Messagebox.yesno("Are you sure you want to delete this assignment?", "Confirm Deletion") == "Yes":
            db_id = self.tree.item(selected[0], "values")[0]
            success, msg = AssignmentService.delete_assignment(db_id)
            if success:
                self.refresh()
            else:
                Messagebox.show_error(msg, "Error")
