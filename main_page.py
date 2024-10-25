import tkinter as tk

def show_main_page(username):

    main_window = tk.Tk()
    main_window.title(f"Office of the Sub Divisional Magistrate, Khategaon")
    main_window.title(f"Welcome {username}")

    
    # Resize the login window for better visibility
    main_window.geometry("800*800")

    # Button to go to Javak Panji
    javak_button = tk.Button(main_window, text="Javak Panji", command=lambda: show_javak_panji(username))
    javak_button.grid(row=0, column=0, padx=10, pady=10)

    # Button to go to Aavak Panji
    aavak_button = tk.Button(main_window, text="Aavak Panji", command=lambda: show_aavak_panji(username))
    aavak_button.grid(row=1, column=0, padx=10, pady=10)

    # Button to go to Mooltah Panji 
    mooltah_button = tk.Button(main_window, text="Mooltah Panji", command=lambda: show_mooltah_panji(username))
    mooltah_button.grid(row=2, column=0, padx=10, pady=10)

    # Button to go to Moolatah Panji Dhara 115
    dhara_button = tk.Button(main_window, text="Mooltah Panji Dhara 115", command=lambda: show_dhara_115_panji(username))
    dhara_button.grid(row=3, column=0, padx=10, pady=10)

    main_window.mainloop()

# Import the respective pages to handle page navigation
def show_javak_panji(username):
    import javak_panji
    javak_panji.show_javak_form(username)

def show_aavak_panji(username):
    import aavak_panji
    aavak_panji.show_aavak_form(username)

def show_mooltah_panji(username):
    import mooltah_panji
    mooltah_panji.show_mooltah_form(username)

def show_dhara_115_panji(username):
    import mooltah_panji_115
    mooltah_panji_115.show_dhara_115_form(username)
