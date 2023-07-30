from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
# Replace these with your actual database credentials
DATABASE_HOST = "sql6.freesqldatabase.com"
DATABASE_USER = "sql6636018"
DATABASE_PASSWORD = "s8CLfLZbqj"
DATABASE_NAME = "sql6636018"

# Set a secret key for the session
app.secret_key = "your_secret_key"

# Function to connect to the database and validate user login
def validate_login(username, password):
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = connection.cursor()

        # Replace 'users' with the actual name of your user table
        query = f"SELECT * FROM students WHERE id = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return True

    except mysql.connector.Error as error:
        print(f"Error accessing the database: {error}")

    return False

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_login(username, password):
            # Store the logged-in state in a session variable
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")

@app.route("/home")
def home():
    # Check if the user is logged in before displaying the home page
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    return "Welcome to the home page!"

@app.route("/logout")
def logout():
    # Clear the session data and log the user out
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
