import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from services.course_service import CourseService

class CoursesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="📚 Course Management",
            font=("Segoe UI", 26, "bold")
        ).pack(side=LEFT)

        # FORM CONTAINER
        form_container = ttk.Frame(self, bootstyle="dark", padding=20)
        form_container.pack(fill=X, pady=(0, 25))

        ttk.Label(
            form_container,
            text="Course Details",
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark"
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        self.id_var = ttk.StringVar()
        
        # ROW 1: Code & Name
        ttk.Label(form_container, text="Course Code", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.code_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.code_entry.grid(row=2, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Course Name", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=1, sticky=W)
        self.name_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=40)
        self.name_entry.grid(row=2, column=1, columnspan=2, sticky=W, pady=(5, 15), ipady=5)

        # ROW 2: Description
        ttk.Label(form_container, text="Description", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=0, sticky=NW, padx=(0, 10))
        self.desc_text = ttk.Text(form_container, font=("Segoe UI", 10), width=65, height=3)
        self.desc_text.grid(row=3, column=1, columnspan=2, sticky=W, pady=(5, 15))

        # ACTION BUTTONS
        btn_frame = ttk.Frame(form_container, bootstyle="dark")
        btn_frame.grid(row=4, column=1, columnspan=2, sticky=W, pady=(10, 0))

        ttk.Button(btn_frame, text="💾 Save Course", bootstyle="success", command=self.save_course).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🔄 Clear Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", bootstyle="danger", command=self.delete_course).pack(side=LEFT, ipady=4)

        # DATA TABLE CONTAINER
        table_container = ttk.Frame(self)
        table_container.pack(fill=BOTH, expand=YES)

        columns = ("id", "code", "name", "description")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle="primary"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("code", text="Course Code")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("code", width=150)
        self.tree.column("name", width=300)
        self.tree.column("description", width=400)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        courses = CourseService.get_all_courses()
        for course in courses:
            self.tree.insert("", END, values=(course['id'], course['code'], course['name'], course['description']))
        
        self.clear_form()

    def clear_form(self):
        self.id_var.set("")
        self.code_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.desc_text.delete("1.0", END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.id_var.set(values[0])
            self.code_entry.insert(0, values[1])
            self.name_entry.insert(0, values[2])
            self.desc_text.insert("1.0", values[3])

    def save_course(self):
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        description = self.desc_text.get("1.0", END).strip()
        course_id = self.id_var.get()

        if not code or not name:
            Messagebox.show_error("Course Code and Name are required.", "Validation Error")
            return

        if course_id:
            success, msg = CourseService.update_course(course_id, code, name, description)
        else:
            success, msg = CourseService.add_course(code, name, description)

        if success:
            Messagebox.show_info(msg, "Success")
            self.refresh()
        else:
            Messagebox.show_error(msg, "Database Error")

    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select a course to delete from the list below.", "No Selection")
            return
            
        if Messagebox.yesno("Are you sure you want to permanently delete this course?", "Confirm Deletion") == "Yes":
            course_id = self.tree.item(selected[0], "values")[0]
            success, msg = CourseService.delete_course(course_id)
            if success:
                self.refresh()
            else:
                Messagebox.show_error(msg, "Deletion Error")
