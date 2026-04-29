import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from services.announcement_service import AnnouncementService

class AnnouncementsView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="📢 Announcements Board",
            font=("Segoe UI", 26, "bold")
        ).pack(side=LEFT)

        # FORM CONTAINER
        form_container = ttk.Frame(self, bootstyle="dark", padding=20)
        form_container.pack(fill=X, pady=(0, 25))

        ttk.Label(
            form_container,
            text="Post Announcement",
            font=("Segoe UI", 14, "bold"),
            bootstyle="inverse-dark"
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        self.id_var = ttk.StringVar()
        
        # ROW 1: Title & Date
        ttk.Label(form_container, text="Title", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.title_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=40)
        self.title_entry.grid(row=2, column=0, sticky=W, padx=(0, 20), pady=(5, 15), ipady=5)

        ttk.Label(form_container, text="Date (YYYY-MM-DD)", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=1, column=1, sticky=W)
        self.date_entry = ttk.Entry(form_container, font=("Segoe UI", 10), width=20)
        self.date_entry.grid(row=2, column=1, sticky=W, pady=(5, 15), ipady=5)

        # ROW 2: Content
        ttk.Label(form_container, text="Message Content", font=("Segoe UI", 10), bootstyle="inverse-dark").grid(row=3, column=0, sticky=NW, padx=(0, 10))
        self.content_text = ttk.Text(form_container, font=("Segoe UI", 10), width=65, height=4)
        self.content_text.grid(row=3, column=1, columnspan=2, sticky=W, pady=(5, 15))

        # ACTION BUTTONS
        btn_frame = ttk.Frame(form_container, bootstyle="dark")
        btn_frame.grid(row=4, column=1, columnspan=2, sticky=W, pady=(10, 0))

        ttk.Button(btn_frame, text="💾 Post Announcement", bootstyle="success", command=self.save_announcement).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🔄 Clear Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=(0, 10), ipady=4)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", bootstyle="danger", command=self.delete_announcement).pack(side=LEFT, ipady=4)

        # DATA TABLE
        table_container = ttk.Frame(self)
        table_container.pack(fill=BOTH, expand=YES)

        columns = ("id", "title", "content", "date")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle="warning"
        )
        
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("content", text="Message Content")
        self.tree.heading("date", text="Date Posted")

        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("title", width=250)
        self.tree.column("content", width=400)
        self.tree.column("date", width=120, anchor=CENTER)

        scrollbar = ttk.Scrollbar(table_container, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        announcements = AnnouncementService.get_all_announcements()
        for a in announcements:
            self.tree.insert("", END, values=(a['id'], a['title'], a['content'], a['date']))
        
        self.clear_form()

    def clear_form(self):
        self.id_var.set("")
        self.title_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.content_text.delete("1.0", END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.id_var.set(values[0])
            self.title_entry.insert(0, values[1])
            self.content_text.insert("1.0", values[2])
            self.date_entry.insert(0, values[3])

    def save_announcement(self):
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        content = self.content_text.get("1.0", END).strip()
        db_id = self.id_var.get()

        if not title or not content or not date:
            Messagebox.show_error("Title, Content, and Date are required fields.", "Validation Error")
            return

        if db_id:
            success, msg = AnnouncementService.update_announcement(db_id, title, content, date)
        else:
            success, msg = AnnouncementService.add_announcement(title, content, date)

        if success:
            self.refresh()
        else:
            Messagebox.show_error(msg, "Error")

    def delete_announcement(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_warning("Please select an announcement to delete.", "No Selection")
            return
            
        if Messagebox.yesno("Are you sure you want to permanently delete this announcement?", "Confirm Deletion") == "Yes":
            db_id = self.tree.item(selected[0], "values")[0]
            success, msg = AnnouncementService.delete_announcement(db_id)
            if success:
                self.refresh()
            else:
                Messagebox.show_error(msg, "Error")
