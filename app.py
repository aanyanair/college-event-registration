from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP default
        database="event_registration"
    )


# Home Route
@app.route("/")
def home():
    return render_template("index.html")


# Register Route
@app.route("/register", methods=["POST"])
def register():
    try:
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        ku_id = request.form.get("ku_id")
        event = request.form.get("event")

        # Connect database
        db = get_db_connection()
        cursor = db.cursor()

        # SQL Query
        sql = """
        INSERT INTO registrations
        (name, email, department, ku_id, event_name)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (name, email, department, ku_id, event)

        cursor.execute(sql, values)
        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "status": "success"
        })

    except Exception as e:
        print("Database Error:", e)

        return jsonify({
            "status": "error"
        })


# Run Server
if __name__ == "__main__":
    app.run(debug=True)