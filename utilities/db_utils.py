import sqlite3

# Path to the database file
DB_PATH = "app_data.db"  # Ensure all functions use this path

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Create table for Javak Panji, add similar for others
    c.execute('''
    CREATE TABLE IF NOT EXISTS javak_panji (
        serial_no INTEGER PRIMARY KEY AUTOINCREMENT,
        javak_no TEXT NOT NULL,
        date TEXT NOT NULL,
        kisko_bheja_gaya TEXT NOT NULL,
        patra_ka_vivaran TEXT NOT NULL,
        tapaal_no TEXT NOT NULL,
        submitted_by TEXT NOT NULL,
        submitted_on TEXT NOT NULL
    )
    ''')
    
    # Add table creation for Aavak Panji, Mooltah Panji, etc.
    
    conn.commit()
    conn.close()

def check_user_exists(username):
    conn = sqlite3.connect(DB_PATH)  # Use the correct DB file
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)  # Use the correct DB file
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect(DB_PATH)  # Use the correct DB file
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None


def add_javak_panji(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO javak_panji (javak_no, date, kisko_bheja_gaya, patra_ka_vivaran, tapaal_no, submitted_by, submitted_on) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_aavak_panji(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO aavak_panji (aavak_no, karyalay_me_amad_dinank, patra_kramank_evam_dinank, kaha_se_prapt, patra_ka_vivaran, submitted_by, submitted_on) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_mooltah_panji(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO mooltah_panji (kramank, karyalay_ka_amad_kramank_ewam_dinank, kis_shakha_vibhag_karyalay_ko_bheja_gaya, shakha_vibhag_karyalay_ko_bhejne_ka_dinank, submitted_by, submitted_on) VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_mooltah_panji_115(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO mooltah_panji_115 (kramank, bhejne_ka_dinank, kise_bheja_gaya, gaon_ka_naam, prarthi_ka_naam_ewam_awedan_ka_vivaran, submitted_by, submitted_on) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
