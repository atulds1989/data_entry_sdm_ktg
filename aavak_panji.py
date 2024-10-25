import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import pandas as pd  
from tkinter import filedialog
from tkcalendar import DateEntry  
# import datetime
from datetime import datetime

# File to store entries
ENTRY_FILE = "aavak_entries.json"

# Load existing entries from the JSON file
def load_entries():
    if os.path.exists(ENTRY_FILE):
        with open(ENTRY_FILE, "r") as file:
            return json.load(file)
    return []

# Save entries to the JSON file
def save_entries_to_file(entries):
    with open(ENTRY_FILE, "w") as file:
        json.dump(entries, file)

# Initialize entries from the file
aavak_entries = load_entries()

# Global variables for entry fields and Treeview
aavak_no_entry = None
date_entry = None  # This will now be a DateEntry
patra_kramank_dinak = None
kaha_se_prapt_entry = None
vivran_entry = None
entries_tree = None


def show_aavak_form(username):
    global aavak_no_entry, date_entry, patra_kramank_dinak, kaha_se_prapt_entry, vivran_entry
    aavak_window = tk.Tk()
    aavak_window.title("Aavak Panji")

    # Set the window to a larger size
    aavak_window.geometry("1200x700")  # Width x Height

#  labels = ["Aavak No", "Karyalay Me Amad Dinank", "Patra Kramank evam Dinank", "Kaha se Prapt", "Patra Ka Vivaran"]

    # Entry fields for Aavak Panji
    aavak_no_label = tk.Label(aavak_window, text="Aavak No:")
    aavak_no_label.grid(row=0, column=0, padx=10, pady=10)
    aavak_no_entry = tk.Entry(aavak_window, width=30)
    aavak_no_entry.grid(row=0, column=1, padx=10, pady=10)

    date_label = tk.Label(aavak_window, text="Karyalay Me Amad Dinank (Date) (DD/MM/YYYY):")
    date_label.grid(row=1, column=0, padx=10, pady=10)

    # Use DateEntry for date input
    date_entry = DateEntry(aavak_window, width=30, date_pattern='dd/mm/yyyy')  # Date format
    date_entry.grid(row=1, column=1, padx=10, pady=10)

    kisko_bheja_label = tk.Label(aavak_window, text="Patra Kramank evam Dinank:")
    kisko_bheja_label.grid(row=2, column=0, padx=10, pady=10)
    kisko_bheja_entry = tk.Entry(aavak_window, width=30)
    kisko_bheja_entry.grid(row=2, column=1, padx=10, pady=10)

    patra_ka_vivaran_label = tk.Label(aavak_window, text="Kaha se Prapt:")
    patra_ka_vivaran_label.grid(row=3, column=0, padx=10, pady=10)
    patra_ka_vivaran_entry = tk.Text(aavak_window, width=30, height=4)  
    patra_ka_vivaran_entry.grid(row=3, column=1, padx=10, pady=10)

    tapaal_no_label = tk.Label(aavak_window, text="Patra Ka Vivaran:")
    tapaal_no_label.grid(row=4, column=0, padx=10, pady=10)
    tapaal_no_entry = tk.Entry(aavak_window, width=30)
    tapaal_no_entry.grid(row=4, column=1, padx=10, pady=10)

    # Create a Treeview to display existing entries in a tabular format
    columns = ("Aavak No", "Karyalay Me Amad Dinank", "Patra Kramank evam Dinank", "Kaha se Prapt", "Patra Ka Vivaran")
    entries_tree = ttk.Treeview(aavak_window, columns=columns, show="headings")
    for col in columns:
        entries_tree.heading(col, text=col)
        entries_tree.column(col, anchor="center")

    # Set the Treeview to fill the entire width of the window
    entries_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    # Expand the Treeview to fill available space
    aavak_window.grid_rowconfigure(8, weight=1)
    aavak_window.grid_columnconfigure(0, weight=1)
    aavak_window.grid_columnconfigure(1, weight=1)

    # Button row
    button_frame = tk.Frame(aavak_window)
    button_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Button to save the entry
    save_button = tk.Button(button_frame, text="Save Entry", command=save_entry, width=15)
    save_button.grid(row=0, column=0, padx=10, pady=10)

    # Button to update the entry
    update_button = tk.Button(button_frame, text="Update Entry", command=update_entry, width=15)
    update_button.grid(row=0, column=1, padx=10, pady=10)

    # Button to delete the entry
    delete_button = tk.Button(button_frame, text="Delete Entry", command=delete_entry, width=15)
    delete_button.grid(row=0, column=2, padx=10, pady=10)

    # Button to clear the fields
    clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_entries, width=15)
    clear_button.grid(row=0, column=3, padx=10, pady=10)

    # Button to download entries to Excel
    download_button = tk.Button(button_frame, text="Download to Excel", command=download_entries, width=15)
    download_button.grid(row=0, column=4, padx=10, pady=10)

    # Bind the selection event
    entries_tree.bind("<<TreeviewSelect>>", on_select)

    update_entries_display()  # Load existing entries on startup

    aavak_window.mainloop()

# Check for unique aavak No
def is_aavak_no_unique(aavak_no):
    for entry in aavak_entries:
        if entry['aavak_no'] == aavak_no:
            return False
    return True

# Save entry function
def save_entry():
    aavak_no = aavak_no_entry.get()
    if not is_aavak_no_unique(aavak_no):
        messagebox.showwarning("Duplicate Entry", "aavak No must be unique!")
        return


#  labels = ["Aavak No", "Karyalay Me Amad Dinank", "Patra Kramank evam Dinank", "Kaha se Prapt", "Patra Ka Vivaran"]


    entry = {
        "aavak_no": aavak_no,
        "date": date_entry.get(),  # Get date from DateEntry
        "kisko_bheja": patra_kramank_dinak.get(),
        "patra_ka_vivaran": kaha_se_prapt_entry.get("1.0", tk.END).strip(),  # Get text from Text widget
        "tapaal_no": vivran_entry.get(),
    }


    aavak_entries.append(entry)
    save_entries_to_file(aavak_entries)  # Save to file
    messagebox.showinfo("Success", "Entry saved!")
    clear_entries()
    update_entries_display()

    # # Global variables for entry fields and Treeview
# aavak_no_entry = None
# date_entry = None  # This will now be a DateEntry
# patra_kramank_dinak = None
# kaha_se_prapt_entry = None
# vivran_entry = None


# Clear entries function
def clear_entries():
    aavak_no_entry.delete(0, tk.END)
    date_entry.set_date(datetime.now())  # Reset to today's date
    patra_kramank_dinak.delete(0, tk.END)
    kaha_se_prapt_entry.delete("1.0", tk.END)  # Clear Text widget
    vivran_entry.delete(0, tk.END)

# Update entries display function
def update_entries_display():
    # Clear the tree view before updating
    for row in entries_tree.get_children():
        entries_tree.delete(row)

    for entry in aavak_entries:
        entries_tree.insert("", tk.END, values=(entry['aavak_no'], entry['date'],
                                                  entry['kisko_bheja'], 
                                                  entry['patra_ka_vivaran'], 
                                                  entry['tapaal_no']))

# Select entry function
def on_select(event):
    selected_item = entries_tree.selection()
    if selected_item:
        item_values = entries_tree.item(selected_item, "values")
        aavak_no_entry.delete(0, tk.END)
        aavak_no_entry.insert(0, item_values[0])
        date_entry.set_date(item_values[1])  # Set date in DateEntry
        patra_kramank_dinak.delete(0, tk.END)
        patra_kramank_dinak.insert(0, item_values[2])
        kaha_se_prapt_entry.delete("1.0", tk.END)  # Clear Text widget
        kaha_se_prapt_entry.insert("1.0", item_values[3])  # Insert existing data
        vivran_entry.delete(0, tk.END)
        vivran_entry.insert(0, item_values[4])

# Update entry function
def update_entry():
    selected_item = entries_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an entry to update.")
        return

    entry_index = entries_tree.index(selected_item)
    aavak_no = aavak_no_entry.get()

    if not is_aavak_no_unique(aavak_no):
        messagebox.showwarning("Duplicate Entry", "aavak No must be unique!")
        return


    entry = {
        "aavak_no": aavak_no,
        "date": date_entry.get(),  # Get date from DateEntry
        "kisko_bheja": patra_kramank_dinak.get(),
        "patra_ka_vivaran": kaha_se_prapt_entry.get("1.0", tk.END).strip(),  # Get text from Text widget
        "tapaal_no": vivran_entry.get(),
    }

    # Update the entry in the list
    aavak_entries[entry_index] = entry
    save_entries_to_file(aavak_entries)  # Save to file
    messagebox.showinfo("Success", "Entry updated!")
    clear_entries()
    update_entries_display()

# Delete entry function
def delete_entry():
    selected_item = entries_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an entry to delete.")
        return

    entry_index = entries_tree.index(selected_item)
    confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
    if confirmation:
        del aavak_entries[entry_index]
        save_entries_to_file(aavak_entries)  # Save to file
        messagebox.showinfo("Success", "Entry deleted!")
        clear_entries()
        update_entries_display()

# Download to Excel function
def download_entries():
    # Convert entries to DataFrame
    df = pd.DataFrame(aavak_entries)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Entries downloaded successfully!")

# # Example usage
# show_aavak_form("username")
















###############################################


# import tkinter as tk
# from tkinter import messagebox
# from utilities import db_utils
# from datetime import datetime

# def show_aavak_form(username):
#     # Create the Aavak Panji form window
#     form_window = tk.Toplevel()
#     form_window.title("Aavak Panji")

#     labels = ["Aavak No", "Karyalay Me Amad Dinank", "Patra Kramank evam Dinank", "Kaha se Prapt", "Patra Ka Vivaran"]
#     entries = []

#     for idx, label in enumerate(labels):
#         tk.Label(form_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
#         entry = tk.Entry(form_window)
#         entry.grid(row=idx, column=1, padx=10, pady=5)
#         entries.append(entry)

#     # Function to save data
#     def save_aavak_panji():
#         data = [
#             entries[0].get(),  # Aavak No
#             entries[1].get(),  # Karyalay Me Amad Dinank
#             entries[2].get(),  # Patra Kramank evam Dinank
#             entries[3].get(),  # Kaha se Prapt
#             entries[4].get(),  # Patra Ka Vivaran
#             username,  # Submitted by (auto-filled)
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Submitted on (auto-filled)
#         ]
        
#         if all(data):  # Ensure all fields are filled
#             db_utils.add_aavak_panji(data)
#             messagebox.showinfo("Success", "Data saved successfully!")
#         else:
#             messagebox.showerror("Error", "All fields must be filled!")

#     # Add a submit button
#     submit_button = tk.Button(form_window, text="Submit", command=save_aavak_panji)
#     submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

#     form_window.mainloop()
