import login
from utilities import db_utils

# Initialize the database before starting the app
db_utils.init_db()


if __name__ == "__main__":
    login.show_login()  # This will show the login/sign-up form



# set PYINSTALLER_USER_DIR=C:\Users\<YourUsername>\AppData\Local\pyinstaller
# pyinstaller --onefile app.py

# pyinstaller --onefile --windowed app.py
