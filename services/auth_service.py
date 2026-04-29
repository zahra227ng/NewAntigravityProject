from models.user import User

class AuthService:
    @staticmethod
    def login(username, password):
        # Mock login: accepts admin / admin123
        if username == "admin" and password == "admin123":
            return User(1, "admin", "admin"), "Login successful"
        return None, "Invalid username or password"
