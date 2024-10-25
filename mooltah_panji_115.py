import tkinter as tk
from tkinter import messagebox
from utilities import db_utils
from datetime import datetime

def show_mooltah_panji_115_form(username):
    # Create the Mooltah Panji Dhara 115 form window
    form_window = tk.Toplevel()
    form_window.title("Mooltah Panji Dhara 115")

    labels = ["Kramank", "Bhejne ka Dinank", "Kise Bheja Gaya", "Gaon ka Naam", "Prarthi Ka Naam Ewam Awedan Ka Vivaran"]
    entries = []

    for idx, label in enumerate(labels):
        tk.Label(form_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(form_window)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries.append(entry)

    # Function to save data
    def save_mooltah_panji_115():
        data = [
            entries[0].get(),  # Kramank
            entries[1].get(),  # Bhejne ka Dinank
            entries[2].get(),  # Kise Bheja Gaya
            entries[3].get(),  # Gaon ka Naam
            entries[4].get(),  # Prarthi Ka Naam Ewam Awedan Ka Vivaran
            username,  # Submitted by (auto-filled)
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Submitted on (auto-filled)
        ]
        
        if all(data):  # Ensure all fields are filled
            db_utils.add_mooltah_panji_115(data)
            messagebox.showinfo("Success", "Data saved successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    # Add a submit button
    submit_button = tk.Button(form_window, text="Submit", command=save_mooltah_panji_115)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    form_window.mainloop()
