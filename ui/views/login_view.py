import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from services.auth_service import AuthService

class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # MAIN CONTAINER
        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        # CENTER CARD
        center_card = ttk.Frame(container, padding=50, bootstyle="dark")
        center_card.pack(fill=BOTH, expand=YES)

        # LOGO / TITLE
        ttk.Label(
            center_card,
            text="🔐",
            font=("Segoe UI", 48)
        ).pack(pady=(0, 10))

        title = ttk.Label(
            center_card,
            text="Welcome Back",
            font=("Segoe UI", 24, "bold"),
            bootstyle="inverse-dark"
        )
        title.pack(pady=(0, 30))

        # USERNAME
        ttk.Label(
            center_card,
            text="Username",
            font=("Segoe UI", 10),
            bootstyle="inverse-dark"
        ).pack(anchor=W, pady=(0, 5))
        
        self.username_var = ttk.StringVar()
        self.username_entry = ttk.Entry(
            center_card,
            textvariable=self.username_var,
            font=("Segoe UI", 11),
            width=35
        )
        self.username_entry.pack(ipady=8, pady=(0, 15))

        # PASSWORD
        ttk.Label(
            center_card,
            text="Password",
            font=("Segoe UI", 10),
            bootstyle="inverse-dark"
        ).pack(anchor=W, pady=(0, 5))

        self.password_var = ttk.StringVar()
        self.password_entry = ttk.Entry(
            center_card,
            textvariable=self.password_var,
            show="•",
            font=("Segoe UI", 11),
            width=35
        )
        self.password_entry.pack(ipady=8, pady=(0, 5))

        # ERROR MESSAGE
        self.error_label = ttk.Label(
            center_card,
            text="",
            font=("Segoe UI", 10),
            bootstyle="danger-inverse"
        )
        self.error_label.pack(pady=5)

        # LOGIN BUTTON
        login_btn = ttk.Button(
            center_card,
            text="Sign In",
            bootstyle="primary",
            command=self.handle_login
        )
        login_btn.pack(fill=X, pady=(15, 0), ipady=8)
        
        # BINDINGS
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            self.error_label.config(text="Please fill in all fields")
            return

        user, message = AuthService.login(username, password)
        if user:
            self.error_label.config(text="")
            self.username_var.set("")
            self.password_var.set("")
            self.controller.on_login_success(user)
        else:
            self.error_label.config(text=message)
