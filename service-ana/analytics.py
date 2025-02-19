import time
import os
import mysql.connector
from pymongo import MongoClient
from mysql.connector import Error
from threading import Thread

# Connect to MySQL
try:
    mysql_conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    print("Connected to MySQL.")
except Error as e:
    print(f"Error while connecting to MySQL: {e}")
    exit(1)

# Connect to MongoDB
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
connection_string = f"mongodb://{username}:{password}@{host}:{port}/"

try:
    mongo_client = MongoClient(connection_string)
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

if __name__ == "__main__":
    # Run the background job in a separate thread
    Thread(target=process_data, daemon=True).start()
    
    # Make sure app doesn't exit
    while True:
        time.sleep(1000)
