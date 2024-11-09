import sqlite3

try:
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('student.db')
    print("Connected to the database successfully.")
    
    # Create a cursor object
    cursor = conn.cursor()

    # Create the student table if it doesn't exist
    table_info = '''
                    CREATE TABLE IF NOT EXISTS student
                    (name varchar(25), class varchar(25), section varchar(25), marks INT);
                '''
    cursor.execute(table_info)
    print("Table created successfully (if it didn't already exist).")
    
    # Insert records into the student table
    insert_data = '''
                    INSERT INTO student (name, class, section, marks) 
                    VALUES (?, ?, ?, ?);
                  '''
    
    # Sample records
    records = [
        ('Alice', '10', 'A', 85),
        ('Bob', '10', 'B', 78),
        ('Charlie', '9', 'A', 92),
        ('David', '9', 'B', 88),
        ('Eva', '10', 'A', 90)
    ]
    
    # Execute insertions
    cursor.executemany(insert_data, records)
    print("Records inserted successfully.")

    data = cursor.execute("""select * from student""")

    print("The inserted records are")
    for row in data:
        print(row)
    
    # Commit changes to the database
    conn.commit()
    
    
except sqlite3.Error as e:
    print("An error occurred:", e)
    
finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
