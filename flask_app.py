from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Function to retrieve temperature data from the database
def get_temperature_data(limit=None):
    try:
        conn = sqlite3.connect('temperature.db')
        cursor = conn.cursor()

        if limit is None:
            cursor.execute("SELECT * FROM temperature ORDER BY timestamp DESC")
        else:
            cursor.execute("SELECT * FROM temperature ORDER BY timestamp DESC LIMIT ?", (limit,))

        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"Error retrieving data from the database: {str(e)}")
        return []

@app.route('/temperature')
def get_temperature():
    try:
        limit = request.args.get('limit', default=None, type=int)
        data = get_temperature_data(limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

