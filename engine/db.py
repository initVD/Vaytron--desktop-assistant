import sqlite3
import csv

# Connect to database
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# 1. Create System Commands Table
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# 2. Create Web Commands Table
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# 3. Create Contacts Table
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')

# 4. Create Personal Info Table
query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
cursor.execute(query)

# Save changes
con.commit()
con.close()

print("Database created successfully!")