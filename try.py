import tkinter as tk
from tkinter import messagebox
import csv
from openpyxl import load_workbook
import os

# Login credentials (change these if you want)
USERNAME = "admin"
PASSWORD = "123"

# Path to save the data (Excel file)
FILE_PATH = "data.xlsx"

# Function to handle login
def login():
    # Check if credentials match the hardcoded username and password
    if username_entry.get() == USERNAME and password_entry.get() == PASSWORD:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()  # Close login window
        open_data_entry_form()  # Open the data entry form
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# Function to save data to Excel file
def save_data():
    data = [
        s_no_entry.get(),
        javak_no_entry.get(),
        date_entry.get(),
        tapaal_no_entry.get(),
        bheja_gaya_entry.get(),
        vivaran_entry.get(),
        submitted_by_entry.get(),
        submitted_on_entry.get()
    ]

    if all(data):  # Check if all fields are filled
        if not os.path.exists(FILE_PATH):
            # Create new Excel file if it doesn't exist
            with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["S.No.", "Javak No", "Date", "Tapaal No", "Kise Bheja Gaya", "Vivaran", "Submitted by", "Submitted on"])
        
        # Append the data to the Excel/CSV file
        with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
        messagebox.showinfo("Success", "Data saved successfully!")
    else:
        messagebox.showerror("Error", "All fields must be filled!")

# Function to create the data entry form
def open_data_entry_form():
    global s_no_entry, javak_no_entry, date_entry, tapaal_no_entry, bheja_gaya_entry, vivaran_entry, submitted_by_entry, submitted_on_entry

    entry_form = tk.Tk()
    entry_form.title("Data Entry Form")

    # Create labels and entry fields for each data field
    labels = ["S.No.", "Javak No", "Date", "Tapaal No", "Kise Bheja Gaya", "Vivaran", "Submitted by", "Submitted on"]
    entries = []

    for idx, label in enumerate(labels):
        tk.Label(entry_form, text=label).grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(entry_form)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries.append(entry)

    # Assign entries to global variables for data extraction
    s_no_entry, javak_no_entry, date_entry, tapaal_no_entry, bheja_gaya_entry, vivaran_entry, submitted_by_entry, submitted_on_entry = entries

    # Add submit button to save data
    submit_button = tk.Button(entry_form, text="Submit", command=save_data)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Set window size for the form
    entry_form.geometry("400x300")
    entry_form.mainloop()

# Main login window
login_window = tk.Tk()
login_window.title("Login")

# Resize the login window for better visibility
login_window.geometry("300x150")

# Username and password fields
tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1)

tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1)

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
