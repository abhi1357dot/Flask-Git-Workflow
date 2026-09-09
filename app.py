from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get MongoDB URL from .env
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is not found. Check your .env file.")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URL)

# Select database
db = client["student_database"]

# Select collection
collection = db["students"]


@app.route("/", methods=["GET", "POST"])
def form():

    error = None

    if request.method == "POST":

        try:
            # Get data from frontend form
            name = request.form.get("name")
            email = request.form.get("email")
            course = request.form.get("course")

            # Validate input
            if not name or not email or not course:
                error = "All fields are required."
                return render_template("form.html", error=error)

            # Insert data into MongoDB
            collection.insert_one({
                "name": name,
                "email": email,
                "course": course
            })

            # Redirect to success page
            return redirect(url_for("success"))

        except Exception as e:
            # Display error on the same page
            error = f"Error: {str(e)}"
            return render_template("form.html", error=error)

    return render_template("form.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)