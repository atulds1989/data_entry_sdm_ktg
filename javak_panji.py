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
ENTRY_FILE = "javak_entries.json"

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
javak_entries = load_entries()

# Global variables for entry fields and Treeview
javak_no_entry = None
date_entry = None  # This will now be a DateEntry
kisko_bheja_entry = None
patra_ka_vivaran_entry = None
tapaal_no_entry = None
entries_tree = None

def show_javak_form(username):
    global javak_no_entry, date_entry, kisko_bheja_entry, patra_ka_vivaran_entry, tapaal_no_entry, entries_tree
    javak_window = tk.Tk()
    javak_window.title("Javak Panji")

    # Set the window to a larger size
    javak_window.geometry("1200x700")  # Width x Height

    # Entry fields for Javak Panji
    javak_no_label = tk.Label(javak_window, text="Javak No:")
    javak_no_label.grid(row=0, column=0, padx=10, pady=10)
    javak_no_entry = tk.Entry(javak_window, width=30)
    javak_no_entry.grid(row=0, column=1, padx=10, pady=10)

    date_label = tk.Label(javak_window, text="Date (DD/MM/YYYY):")
    date_label.grid(row=1, column=0, padx=10, pady=10)

    # Use DateEntry for date input
    date_entry = DateEntry(javak_window, width=30, date_pattern='dd/mm/yyyy')  # Date format
    date_entry.grid(row=1, column=1, padx=10, pady=10)

    kisko_bheja_label = tk.Label(javak_window, text="Kisko Bheja Gaya:")
    kisko_bheja_label.grid(row=2, column=0, padx=10, pady=10)
    kisko_bheja_entry = tk.Entry(javak_window, width=30)
    kisko_bheja_entry.grid(row=2, column=1, padx=10, pady=10)

    patra_ka_vivaran_label = tk.Label(javak_window, text="Patra Ka Vivaran:")
    patra_ka_vivaran_label.grid(row=3, column=0, padx=10, pady=10)
    patra_ka_vivaran_entry = tk.Text(javak_window, width=30, height=4)  # Changed to Text widget for more space
    patra_ka_vivaran_entry.grid(row=3, column=1, padx=10, pady=10)

    tapaal_no_label = tk.Label(javak_window, text="Tapaal No:")
    tapaal_no_label.grid(row=4, column=0, padx=10, pady=10)
    tapaal_no_entry = tk.Entry(javak_window, width=30)
    tapaal_no_entry.grid(row=4, column=1, padx=10, pady=10)

    # Create a Treeview to display existing entries in a tabular format
    columns = ("Javak No", "Date", "Kisko Bheja Gaya", "Patra Ka Vivaran", "Tapaal No")
    entries_tree = ttk.Treeview(javak_window, columns=columns, show="headings")
    for col in columns:
        entries_tree.heading(col, text=col)
        entries_tree.column(col, anchor="center")

    # Set the Treeview to fill the entire width of the window
    entries_tree.grid(row=15, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    # Expand the Treeview to fill available space
    javak_window.grid_rowconfigure(8, weight=1)
    javak_window.grid_columnconfigure(0, weight=1)
    javak_window.grid_columnconfigure(1, weight=1)

    # Button row
    button_frame = tk.Frame(javak_window)
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

    javak_window.mainloop()

# Check for unique Javak No
def is_javak_no_unique(javak_no):
    for entry in javak_entries:
        if entry['javak_no'] == javak_no:
            return False
    return True

# Save entry function
def save_entry():
    javak_no = javak_no_entry.get()
    if not is_javak_no_unique(javak_no):
        messagebox.showwarning("Duplicate Entry", "Javak No must be unique!")
        return

    entry = {
        "javak_no": javak_no,
        "date": date_entry.get(),  # Get date from DateEntry
        "kisko_bheja": kisko_bheja_entry.get(),
        "patra_ka_vivaran": patra_ka_vivaran_entry.get("1.0", tk.END).strip(),  # Get text from Text widget
        "tapaal_no": tapaal_no_entry.get(),
    }
    javak_entries.append(entry)
    save_entries_to_file(javak_entries)  # Save to file
    messagebox.showinfo("Success", "Entry saved!")
    clear_entries()
    update_entries_display()

# Clear entries function
def clear_entries():
    javak_no_entry.delete(0, tk.END)
    date_entry.set_date(datetime.now())  # Reset to today's date
    kisko_bheja_entry.delete(0, tk.END)
    patra_ka_vivaran_entry.delete("1.0", tk.END)  # Clear Text widget
    tapaal_no_entry.delete(0, tk.END)

# Update entries display function
def update_entries_display():
    # Clear the tree view before updating
    for row in entries_tree.get_children():
        entries_tree.delete(row)

    for entry in javak_entries:
        entries_tree.insert("", tk.END, values=(entry['javak_no'], entry['date'],
                                                  entry['kisko_bheja'], 
                                                  entry['patra_ka_vivaran'], 
                                                  entry['tapaal_no']))

# Select entry function
def on_select(event):
    selected_item = entries_tree.selection()
    if selected_item:
        item_values = entries_tree.item(selected_item, "values")
        javak_no_entry.delete(0, tk.END)
        javak_no_entry.insert(0, item_values[0])
        date_entry.set_date(item_values[1])  # Set date in DateEntry
        kisko_bheja_entry.delete(0, tk.END)
        kisko_bheja_entry.insert(0, item_values[2])
        patra_ka_vivaran_entry.delete("1.0", tk.END)  # Clear Text widget
        patra_ka_vivaran_entry.insert("1.0", item_values[3])  # Insert existing data
        tapaal_no_entry.delete(0, tk.END)
        tapaal_no_entry.insert(0, item_values[4])

# Update entry function
def update_entry():
    selected_item = entries_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an entry to update.")
        return

    entry_index = entries_tree.index(selected_item)
    javak_no = javak_no_entry.get()

    if not is_javak_no_unique(javak_no):
        messagebox.showwarning("Duplicate Entry", "Javak No must be unique!")
        return

    entry = {
        "javak_no": javak_no,
        "date": date_entry.get(),  # Get date from DateEntry
        "kisko_bheja": kisko_bheja_entry.get(),
        "patra_ka_vivaran": patra_ka_vivaran_entry.get("1.0", tk.END).strip(),  # Get text from Text widget
        "tapaal_no": tapaal_no_entry.get(),
    }

    # Update the entry in the list
    javak_entries[entry_index] = entry
    save_entries_to_file(javak_entries)  # Save to file
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
        del javak_entries[entry_index]
        save_entries_to_file(javak_entries)  # Save to file
        messagebox.showinfo("Success", "Entry deleted!")
        clear_entries()
        update_entries_display()

# Download to Excel function
def download_entries():
    # Convert entries to DataFrame
    df = pd.DataFrame(javak_entries)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Entries downloaded successfully!")

# # Example usage
# show_javak_form("username")




















# import tkinter as tk
# from tkinter import messagebox, ttk
# import json
# import os
# import pandas as pd  
# from tkinter import filedialog

# # File to store entries
# ENTRY_FILE = "javak_entries.json"

# # Load existing entries from the JSON file
# def load_entries():
#     if os.path.exists(ENTRY_FILE):
#         with open(ENTRY_FILE, "r") as file:
#             return json.load(file)
#     return []

# # Save entries to the JSON file
# def save_entries_to_file(entries):
#     with open(ENTRY_FILE, "w") as file:
#         json.dump(entries, file)

# # Initialize entries from the file
# javak_entries = load_entries()

# # Global variables for entry fields and Treeview
# javak_no_entry = None
# date_entry = None
# kisko_bheja_entry = None
# patra_ka_vivaran_entry = None
# tapaal_no_entry = None
# entries_tree = None

# def show_javak_form(username):
#     global javak_no_entry, date_entry, kisko_bheja_entry, patra_ka_vivaran_entry, tapaal_no_entry, entries_tree
#     javak_window = tk.Tk()
#     javak_window.title("Javak Panji")

#     # Set the window to a larger size
#     javak_window.geometry("1200x700")  # Width x Height

#     # Entry fields for Javak Panji
#     javak_no_label = tk.Label(javak_window, text="Javak No:")
#     javak_no_label.grid(row=0, column=0, padx=10, pady=10)
#     javak_no_entry = tk.Entry(javak_window, width=30)
#     javak_no_entry.grid(row=0, column=1, padx=10, pady=10)

#     date_label = tk.Label(javak_window, text="Date:")
#     date_label.grid(row=1, column=0, padx=10, pady=10)
#     date_entry = tk.Entry(javak_window, width=30)
#     date_entry.grid(row=1, column=1, padx=10, pady=10)

#     kisko_bheja_label = tk.Label(javak_window, text="Kisko Bheja Gaya:")
#     kisko_bheja_label.grid(row=2, column=0, padx=10, pady=10)
#     kisko_bheja_entry = tk.Entry(javak_window, width=30)
#     kisko_bheja_entry.grid(row=2, column=1, padx=10, pady=10)

#     patra_ka_vivaran_label = tk.Label(javak_window, text="Patra Ka Vivaran:")
#     patra_ka_vivaran_label.grid(row=3, column=0, padx=10, pady=10)
#     patra_ka_vivaran_entry = tk.Text(javak_window, width=30, height=4)  # Changed to Text widget for more space
#     patra_ka_vivaran_entry.grid(row=3, column=1, padx=10, pady=10)

#     tapaal_no_label = tk.Label(javak_window, text="Tapaal No:")
#     tapaal_no_label.grid(row=4, column=0, padx=10, pady=10)
#     tapaal_no_entry = tk.Entry(javak_window, width=30)
#     tapaal_no_entry.grid(row=4, column=1, padx=10, pady=10)

#     # Create a Treeview to display existing entries in a tabular format
#     columns = ("Javak No", "Date", "Kisko Bheja Gaya", "Patra Ka Vivaran", "Tapaal No")
#     entries_tree = ttk.Treeview(javak_window, columns=columns, show="headings")
#     for col in columns:
#         entries_tree.heading(col, text=col)
#         entries_tree.column(col, anchor="center")

#     # Set the Treeview to fill the entire width of the window
#     entries_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

#     # Expand the Treeview to fill available space
#     javak_window.grid_rowconfigure(8, weight=1)
#     javak_window.grid_columnconfigure(0, weight=1)
#     javak_window.grid_columnconfigure(1, weight=1)

#     # Button row
#     button_frame = tk.Frame(javak_window)
#     button_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

#     # Button to save the entry
#     save_button = tk.Button(button_frame, text="Save Entry", command=save_entry, width=15)
#     save_button.grid(row=0, column=0, padx=10, pady=10)

#     # Button to update the entry
#     update_button = tk.Button(button_frame, text="Update Entry", command=update_entry, width=15)
#     update_button.grid(row=0, column=1, padx=10, pady=10)

#     # Button to delete the entry
#     delete_button = tk.Button(button_frame, text="Delete Entry", command=delete_entry, width=15)
#     delete_button.grid(row=0, column=2, padx=10, pady=10)

#     # Button to clear the fields
#     clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_entries, width=15)
#     clear_button.grid(row=0, column=3, padx=10, pady=10)

#     # Button to download entries to Excel
#     download_button = tk.Button(button_frame, text="Download to Excel", command=download_entries, width=15)
#     download_button.grid(row=0, column=4, padx=10, pady=10)

#     # Bind the selection event
#     entries_tree.bind("<<TreeviewSelect>>", on_select)

#     update_entries_display()  # Load existing entries on startup

#     javak_window.mainloop()

# # Check for unique Javak No
# def is_javak_no_unique(javak_no):
#     for entry in javak_entries:
#         if entry['javak_no'] == javak_no:
#             return False
#     return True

# # Save entry function
# def save_entry():
#     javak_no = javak_no_entry.get()
#     if not is_javak_no_unique(javak_no):
#         messagebox.showwarning("Duplicate Entry", "Javak No must be unique!")
#         return

#     entry = {
#         "javak_no": javak_no,
#         "date": date_entry.get(),
#         "kisko_bheja": kisko_bheja_entry.get(),
#         "patra_ka_vivaran": patra_ka_vivaran_entry.get("1.0", tk.END).strip(),  # Get text from Text widget
#         "tapaal_no": tapaal_no_entry.get(),
#     }
#     javak_entries.append(entry)
#     save_entries_to_file(javak_entries)  # Save to file
#     messagebox.showinfo("Success", "Entry saved!")
#     clear_entries()
#     update_entries_display()

# # Clear entries function
# def clear_entries():
#     javak_no_entry.delete(0, tk.END)
#     date_entry.delete(0, tk.END)
#     kisko_bheja_entry.delete(0, tk.END)
#     patra_ka_vivaran_entry.delete("1.0", tk.END)  # Clear Text widget
#     tapaal_no_entry.delete(0, tk.END)

# # Update entries display function
# def update_entries_display():
#     # Clear the tree view before updating
#     for row in entries_tree.get_children():
#         entries_tree.delete(row)

#     for entry in javak_entries:
#         entries_tree.insert("", tk.END, values=(entry['javak_no'], entry['date'],
#                                                   entry['kisko_bheja'], 
#                                                   entry['patra_ka_vivaran'], 
#                                                   entry['tapaal_no']))

# # Select entry function
# def on_select(event):
#     selected_item = entries_tree.selection()
#     if selected_item:
#         item_values = entries_tree.item(selected_item, "values")
#         javak_no_entry.delete(0, tk.END)
#         javak_no_entry.insert(0, item_values[0])
#         date_entry.delete(0, tk.END)
#         date_entry.insert(0, item_values[1])
#         kisko_bheja_entry.delete(0, tk.END)
#         kisko_bheja_entry.insert(0, item_values[2])
#         patra_ka_vivaran_entry.delete("1.0", tk.END)  # Clear Text widget
#         patra_ka_vivaran_entry.insert("1.0", item_values[3])  # Insert text
#         tapaal_no_entry.delete(0, tk.END)
#         tapaal_no_entry.insert(0, item_values[4])

# # # Update entry function
# # def update_entry():
# #     selected_item = entries_tree.selection()
# #     if selected_item:
# #         index = entries_tree.index(selected_item)
# #         javak_no = javak_no_entry.get()
        
# #         if not is_javak_no_unique(javak_no):
# #             messagebox.showwarning("Duplicate Entry", "Javak No must be unique!")
# #             return

# #         javak_entries[index]['javak_no'] = javak_no
# #         javak_entries[index]['date'] = date_entry.get()
# #         javak_entries[index]['kisko_bheja'] = kisko_bheja_entry.get()
# #         javak_entries[index]['patra_ka_vivaran'] = patra_ka_vivaran_entry.get("1.0", tk.END).strip()
# #         javak_entries[index]['tapaal_no'] = tapaal_no_entry.get()
# #         save_entries_to_file(javak_entries)
# #         messagebox.showinfo("Success", "Entry updated!")
# #         clear_entries()
# #         update_entries_display()


# # Update entry function
# def update_entry():
#     selected_item = entries_tree.selection()
#     if selected_item:
#         index = entries_tree.index(selected_item)
#         current_javak_no = javak_entries[index]['javak_no']
#         new_javak_no = javak_no_entry.get()
        
#         # Check if the Javak No is being changed
#         if new_javak_no != current_javak_no and not is_javak_no_unique(new_javak_no):
#             messagebox.showwarning("Duplicate Entry", "Javak No must be unique!")
#             return

#         # Update the entry
#         javak_entries[index]['javak_no'] = new_javak_no
#         javak_entries[index]['date'] = date_entry.get()
#         javak_entries[index]['kisko_bheja'] = kisko_bheja_entry.get()
#         javak_entries[index]['patra_ka_vivaran'] = patra_ka_vivaran_entry.get("1.0", tk.END).strip()
#         javak_entries[index]['tapaal_no'] = tapaal_no_entry.get()
        
#         save_entries_to_file(javak_entries)
#         messagebox.showinfo("Success", "Entry updated!")
#         clear_entries()
#         update_entries_display()


# # Delete entry function
# def delete_entry():
#     selected_item = entries_tree.selection()
#     if selected_item:
#         index = entries_tree.index(selected_item)
#         if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
#             del javak_entries[index]
#             save_entries_to_file(javak_entries)
#             messagebox.showinfo("Success", "Entry deleted!")
#             clear_entries()
#             update_entries_display()

# # # Download entries to Excel
# # def download_entries():
# #     df = pd.DataFrame(javak_entries)
# #     df.to_excel("javak_entries.xlsx", index=False)
# #     messagebox.showinfo("Success", "Entries downloaded to Excel.")



# # Download entries to Excel
# def download_entries():
#     # Open a file dialog to choose the save location
#     file_path = filedialog.asksaveasfilename(
#         defaultextension=".xlsx", 
#         filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
#         title="Save as"
#     )
    
#     if file_path:  # Check if a file path was selected
#         df = pd.DataFrame(javak_entries)
#         df.to_excel(file_path, index=False)
#         messagebox.showinfo("Success", "Entries downloaded to Excel.")



# # # Call the show_javak_form function
# # show_javak_form("admin")









################################################



# import tkinter as tk
# from tkinter import messagebox, ttk
# import json
# import os

# # File to store entries
# ENTRY_FILE = "javak_entries.json"

# # Load existing entries from the JSON file
# def load_entries():
#     if os.path.exists(ENTRY_FILE):
#         with open(ENTRY_FILE, "r") as file:
#             return json.load(file)
#     return []

# # Save entries to the JSON file
# def save_entries_to_file(entries):
#     with open(ENTRY_FILE, "w") as file:
#         json.dump(entries, file)

# # Initialize entries from the file
# javak_entries = load_entries()

# def show_javak_form(username):
#     javak_window = tk.Tk()
#     javak_window.title("Javak Panji")

#     # Set the window to almost full screen
#     javak_window.geometry("1000x600")  # Width x Height

#     # Entry fields for Javak Panji
#     javak_no_label = tk.Label(javak_window, text="Javak No:")
#     javak_no_label.grid(row=0, column=0, padx=10, pady=10)
#     javak_no_entry = tk.Entry(javak_window, width=30)
#     javak_no_entry.grid(row=0, column=1, padx=10, pady=10)

#     date_label = tk.Label(javak_window, text="Date:")
#     date_label.grid(row=1, column=0, padx=10, pady=10)
#     date_entry = tk.Entry(javak_window, width=30)
#     date_entry.grid(row=1, column=1, padx=10, pady=10)

#     kisko_bheja_label = tk.Label(javak_window, text="Kisko Bheja Gaya:")
#     kisko_bheja_label.grid(row=2, column=0, padx=10, pady=10)
#     kisko_bheja_entry = tk.Entry(javak_window, width=30)
#     kisko_bheja_entry.grid(row=2, column=1, padx=10, pady=10)

#     patra_ka_vivaran_label = tk.Label(javak_window, text="Patra Ka Vivaran:")
#     patra_ka_vivaran_label.grid(row=3, column=0, padx=10, pady=10)
#     patra_ka_vivaran_entry = tk.Entry(javak_window, width=30)
#     patra_ka_vivaran_entry.grid(row=3, column=1, padx=10, pady=10)

#     tapaal_no_label = tk.Label(javak_window, text="Tapaal No:")
#     tapaal_no_label.grid(row=4, column=0, padx=10, pady=10)
#     tapaal_no_entry = tk.Entry(javak_window, width=30)
#     tapaal_no_entry.grid(row=4, column=1, padx=10, pady=10)

#     # Create a Treeview to display existing entries in a tabular format
#     columns = ("Javak No", "Date", "Kisko Bheja Gaya", "Patra Ka Vivaran", "Tapaal No")
#     entries_tree = ttk.Treeview(javak_window, columns=columns, show="headings")
#     for col in columns:
#         entries_tree.heading(col, text=col)
#         entries_tree.column(col, anchor="center")

#     entries_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

#     # Expand the treeview to fill available space
#     javak_window.grid_rowconfigure(6, weight=1)
#     javak_window.grid_columnconfigure(0, weight=1)
#     javak_window.grid_columnconfigure(1, weight=1)

#     def save_entry():
#         # Save entry with all fields
#         entry = {
#             "javak_no": javak_no_entry.get(),
#             "date": date_entry.get(),
#             "kisko_bheja": kisko_bheja_entry.get(),
#             "patra_ka_vivaran": patra_ka_vivaran_entry.get(),
#             "tapaal_no": tapaal_no_entry.get(),
#         }
#         javak_entries.append(entry)
#         save_entries_to_file(javak_entries)  # Save to file
#         messagebox.showinfo("Success", "Entry saved!")
#         clear_entries()
#         update_entries_display()

#     def clear_entries():
#         # Clear all entry fields
#         javak_no_entry.delete(0, tk.END)
#         date_entry.delete(0, tk.END)
#         kisko_bheja_entry.delete(0, tk.END)
#         patra_ka_vivaran_entry.delete(0, tk.END)
#         tapaal_no_entry.delete(0, tk.END)

#     def update_entries_display():
#         # Clear the tree view before updating
#         for row in entries_tree.get_children():
#             entries_tree.delete(row)

#         for entry in javak_entries:
#             entries_tree.insert("", tk.END, values=(entry['javak_no'], entry['date'],
#                                                       entry['kisko_bheja'], 
#                                                       entry['patra_ka_vivaran'], 
#                                                       entry['tapaal_no']))

#     def on_select(event):
#         selected_item = entries_tree.selection()
#         if selected_item:
#             item_values = entries_tree.item(selected_item, "values")
#             javak_no_entry.delete(0, tk.END)
#             javak_no_entry.insert(0, item_values[0])
#             date_entry.delete(0, tk.END)
#             date_entry.insert(0, item_values[1])
#             kisko_bheja_entry.delete(0, tk.END)
#             kisko_bheja_entry.insert(0, item_values[2])
#             patra_ka_vivaran_entry.delete(0, tk.END)
#             patra_ka_vivaran_entry.insert(0, item_values[3])
#             tapaal_no_entry.delete(0, tk.END)
#             tapaal_no_entry.insert(0, item_values[4])

#     def update_entry():
#         selected_item = entries_tree.selection()
#         if selected_item:
#             index = entries_tree.index(selected_item)
#             javak_entries[index] = {
#                 "javak_no": javak_no_entry.get(),
#                 "date": date_entry.get(),
#                 "kisko_bheja": kisko_bheja_entry.get(),
#                 "patra_ka_vivaran": patra_ka_vivaran_entry.get(),
#                 "tapaal_no": tapaal_no_entry.get(),
#             }
#             save_entries_to_file(javak_entries)  # Save to file
#             messagebox.showinfo("Success", "Entry updated!")
#             clear_entries()
#             update_entries_display()
#         else:
#             messagebox.showwarning("Select Entry", "Please select an entry to update.")

#     def delete_entry():
#         selected_item = entries_tree.selection()
#         if selected_item:
#             index = entries_tree.index(selected_item)
#             del javak_entries[index]
#             save_entries_to_file(javak_entries)  # Save to file
#             messagebox.showinfo("Success", "Entry deleted!")
#             clear_entries()
#             update_entries_display()
#         else:
#             messagebox.showwarning("Select Entry", "Please select an entry to delete.")

#     # Button to save the entry
#     save_button = tk.Button(javak_window, text="Save Entry", command=save_entry, width=15)
#     save_button.grid(row=5, column=0, padx=10, pady=10)

#     # Button to update the entry
#     update_button = tk.Button(javak_window, text="Update Entry", command=update_entry, width=15)
#     update_button.grid(row=5, column=1, padx=10, pady=10)

#     # Button to delete the entry
#     delete_button = tk.Button(javak_window, text="Delete Entry", command=delete_entry, width=15)
#     delete_button.grid(row=5, column=2, padx=10, pady=10)

#     # Bind the selection event
#     entries_tree.bind("<<TreeviewSelect>>", on_select)

#     update_entries_display()  # Load existing entries on startup

#     javak_window.mainloop()

