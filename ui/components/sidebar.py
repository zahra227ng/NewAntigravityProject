import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Sidebar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bootstyle="dark", padding=15)
        self.controller = controller

        # TITLE
        ttk.Label(
            self,
            text="📊 CMS Panel",
            font=("Segoe UI", 18, "bold"),
            bootstyle="inverse-dark"
        ).pack(pady=(20, 30))

        # NAVIGATION
        self.buttons = {}
        nav_items = [
            ("🏠 Dashboard", "Dashboard"),
            ("📚 Courses", "Courses"),
            ("🎓 Students", "Students"),
            ("📝 Assignments", "Assignments"),
            ("📊 Grades", "Grades"),
            ("📢 Announcements", "Announcements"),
        ]

        for text, page in nav_items:
            btn = ttk.Button(
                self,
                text=text,
                bootstyle="secondary",
                command=lambda p=page: self.switch(p)
            )
            btn.pack(fill=X, pady=6, ipady=6)
            self.buttons[page] = btn

        # LOGOUT
        ttk.Button(
            self,
            text="🚪 Logout",
            bootstyle="danger",
            command=self.controller.logout
        ).pack(side=BOTTOM, fill=X, pady=20, ipady=6)

    def switch(self, page):
        self.controller.show_frame(page)
        self.highlight_active(page)

    def highlight_active(self, active_page):
        for page, btn in self.buttons.items():
            if page == active_page:
                btn.config(bootstyle="primary")  # ACTIVE
            else:
                btn.config(bootstyle="secondary")