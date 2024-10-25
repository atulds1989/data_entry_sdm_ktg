import tkinter as tk
from tkinter import messagebox
import utilities.db_utils as db_utils



def show_login():
    login_window = tk.Tk()
    login_window.title("Login")
    
    # Resize the login window for better visibility
    login_window.geometry("500x350")

    # Username and password fields for login
    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    # Login button
    login_button = tk.Button(login_window, text="Login", command=lambda: login_user(username_entry.get(), password_entry.get(), login_window))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Sign-up button
    signup_button = tk.Button(login_window, text="Sign Up", command=show_signup)
    signup_button.grid(row=3, column=0, columnspan=2, pady=10)

    login_window.mainloop()

def login_user(username, password, window):
    if db_utils.check_login(username, password):
        messagebox.showinfo("Success", "Login successful!")
        window.destroy()
        # Redirect to main page
        import main_page
        main_page.show_main_page(username)
    else:
        messagebox.showerror("Error", "Invalid credentials")

def show_signup():
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    # Resize the login window for better visibility
    signup_window.geometry("500x350")

    # Username and password fields for sign-up
    tk.Label(signup_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(signup_window)
    username_entry.grid(row=0, column=1)

    tk.Label(signup_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.grid(row=1, column=1)

    signup_button = tk.Button(signup_window, text="Sign Up", command=lambda: signup_user(username_entry.get(), password_entry.get(), signup_window))
    signup_button.grid(row=2, column=0, columnspan=2, pady=10)

def signup_user(username, password, window):
    if db_utils.check_user_exists(username):
        messagebox.showerror("Error", "User already exists!")
    else:
        db_utils.add_user(username, password)
        messagebox.showinfo("Success", "Sign-up successful!")
        window.destroy()
