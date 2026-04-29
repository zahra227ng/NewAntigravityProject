import os
import sys

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import db
from ui.app import MainApp

def main():
    # Initialize UI directly
    # db.connect() # Disabled to run purely as UI demo

    # Start the App
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
