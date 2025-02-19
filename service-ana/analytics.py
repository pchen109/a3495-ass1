import time
import os
import mysql.connector
from pymongo import MongoClient
from mysql.connector import Error
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to MySQL
try:
    mysql_conn = mysql.connector.connect(
        # host=os.getenv("MYSQL_HOST"),
        # user=os.getenv("MYSQL_USER"),
        # password=os.getenv("MYSQL_PASSWORD"),
        # database=os.getenv("MYSQL_DATABASE")
        host="mysqldb",
        user="user",
        password="password",
        database="appdb"
    )
    print("Connected to MySQL.")
except Error as e:
    print(f"Error while connecting to MySQL: {e}")
    exit(1)

# Connect to MongoDB
# Load MongoDB connection details from environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
connection_string = f"mongodb://{username}:{password}@{host}:{port}/"

try:
    mongo_client = MongoClient("mongodb://root:root@mongodb:27017/")
    db = mongo_client.analytics
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error while connecting to MongoDB: {e}")
    exit(1)

# Background job to process stats
def process_data():
    while True:
        try:
            mysql_conn.reconnect()
            cursor = mysql_conn.cursor()
            cursor.execute("SELECT AVG(value), MAX(value), MIN(value) FROM temperatures")
            stats = cursor.fetchone()
            
            if stats:
                db.stats.insert_one({
                    "timestamp": time.time(),
                    "average": float(stats[0]),
                    "max": float(stats[1]),
                    "min": float(stats[2])
                })
                print("Data analyzed")
            else:
                print("No data to analyze")
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(3)  # Run every minute

# # Flask endpoint to get the latest analytics stats
# @app.route("/stats", methods=["GET"])
# def get_stats():
#     latest_stat = db.stats.find().sort("timestamp", -1).limit(1)
#     stat = next(latest_stat, None)

#     if stat:
#         return jsonify({
#             "timestamp": stat["timestamp"],
#             "average": stat["average"],
#             "max": stat["max"],
#             "min": stat["min"]
#         })
#     else:
#         return jsonify({"error": "No data available"}), 404

if __name__ == "__main__":
    from threading import Thread
    # Run the background job in a separate thread
    Thread(target=process_data, daemon=True).start()
    # app.run(host="0.0.0.0", port=3002, debug=True)
