import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from services.student_service import StudentService
from services.course_service import CourseService
from services.assignment_service import AssignmentService
from services.announcement_service import AnnouncementService

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=25)
        self.controller = controller

        # HEADER
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 20))

        self.welcome_label = ttk.Label(
            header,
            text="Dashboard",
            font=("Segoe UI", 26, "bold")
        )
        self.welcome_label.pack(side=LEFT)

        # CARDS CONTAINER
        self.cards_frame = ttk.Frame(self)
        self.cards_frame.pack(fill=X)

        for i in range(4):
            self.cards_frame.columnconfigure(i, weight=1)

        self.stat_cards = {}

        self.create_card("👨‍🎓 Students", 0, "primary")
        self.create_card("📚 Courses", 1, "success")
        self.create_card("📝 Assignments", 2, "info")
        self.create_card("📢 Announcements", 3, "warning")

    def create_card(self, title, col, style):
        card = ttk.Frame(self.cards_frame, padding=20, bootstyle=f"{style}")
        card.grid(row=0, column=col, padx=10, sticky="nsew")

        ttk.Label(
            card,
            text=title,
            font=("Segoe UI", 13),
            bootstyle=f"inverse-{style}"
        ).pack(anchor=W)

        value = ttk.Label(
            card,
            text="0",
            font=("Segoe UI", 28, "bold"),
            bootstyle=f"inverse-{style}"
        )
        value.pack(anchor=W, pady=(10, 0))

        self.stat_cards[title] = value

    def refresh(self):
        if self.controller.current_user:
            self.welcome_label.config(
                text=f"Welcome, {self.controller.current_user.username.capitalize()} 👋"
            )

        try:
            self.stat_cards["👨‍🎓 Students"].config(text=len(StudentService.get_all_students()))
            self.stat_cards["📚 Courses"].config(text=len(CourseService.get_all_courses()))
            self.stat_cards["📝 Assignments"].config(text=len(AssignmentService.get_all_assignments()))
            self.stat_cards["📢 Announcements"].config(text=len(AnnouncementService.get_all_announcements()))
        except Exception as e:
            print("Error loading mock stats:", e)