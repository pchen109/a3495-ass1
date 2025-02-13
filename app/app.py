from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="data_db"
)
cursor = db.cursor()

@app.route("/", methods=["GET"])
def home():
    return "Data Collection API Running!"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json.get("value")
    cursor.execute("INSERT INTO data (value) VALUES (%s)", (data,))
    db.commit()
    return jsonify({"message": "Data saved!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
