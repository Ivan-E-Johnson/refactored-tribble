import sqlite3

# Function to initialize the database
def initialize_database():
    try:
        conn = sqlite3.connect('temperature.db')
        cursor = conn.cursor()
        
        # Create the temperature table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temp_c REAL,
                humidity REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {str(e)}")

if __name__ == '__main__':
    initialize_database()

