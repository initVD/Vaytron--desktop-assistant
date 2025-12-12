import csv
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# 1. Create System Commands Table
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Insert default system commands (Optional: You can comment these out if you run this multiple times)
# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# 2. Create Web Commands Table
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# Insert default web commands
# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()

# 3. Create Contacts Table
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')

# 4. Create Personal Info Table
query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
cursor.execute(query)

con.commit()

# --- OPTIONAL: Import Contacts from CSV (Uncomment only if you have contacts.csv) ---
# desired_columns_indices = [0, 30]
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))
# con.commit()

con.close()
print("Database initialized successfully.")