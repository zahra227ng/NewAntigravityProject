import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.views.login_view import LoginView
from ui.views.dashboard_view import DashboardView
from ui.views.courses_view import CoursesView
from ui.views.students_view import StudentsView
from ui.views.assignments_view import AssignmentsView
from ui.views.grades_view import GradesView
from ui.views.announcements_view import AnnouncementsView
from ui.components.sidebar import Sidebar

class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly", title="Academic Management Dashboard", size=(1200, 800))
        self.current_user = None
        self.frames = {}
        
        # Container for all frames
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.sidebar = None
        self.content_frame = ttk.Frame(self.container)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.show_login()

    def show_login(self):
        if self.sidebar:
            self.sidebar.grid_forget()
        
        for frame in self.frames.values():
            frame.grid_forget()

        login_view = LoginView(self.container, self)
        login_view.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frames["Login"] = login_view

    def on_login_success(self, user):
        self.current_user = user
        self.frames["Login"].grid_forget()
        self.setup_main_layout()

    def setup_main_layout(self):
        # Initialize sidebar
        self.sidebar = Sidebar(self.container, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Initialize views
        self.frames["Dashboard"] = DashboardView(self.content_frame, self)
        self.frames["Courses"] = CoursesView(self.content_frame, self)
        self.frames["Students"] = StudentsView(self.content_frame, self)
        self.frames["Assignments"] = AssignmentsView(self.content_frame, self)
        self.frames["Grades"] = GradesView(self.content_frame, self)
        self.frames["Announcements"] = AnnouncementsView(self.content_frame, self)
        
        # Place all frames in the same grid spot
        for frame_name, frame in self.frames.items():
            if frame_name != "Login":
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            if hasattr(frame, "refresh"):
                frame.refresh()
            frame.tkraise()

    def logout(self):
        self.current_user = None
        self.show_login()
