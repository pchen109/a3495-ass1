from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT")
connection_string = f"mongodb://{username}:{password}@{host}:{port}/"
client = MongoClient("mongodb://root:root@mongodb:27017/")
db = client.analytics

@app.route('/stats', methods=['GET'])
def get_stats():
    stats = db.stats.find().sort("timestamp", -1).limit(1)
    # Get the first document or None if no document is found
    stat = next(stats, None)  

    if stat:
        return jsonify({
            "id": str(stat["_id"]),
            "timestamp": stat["timestamp"],
            "average": stat["average"],
            "max": stat["max"],
            "min": stat["min"]
        })
    else:
        return jsonify({"error": "No data available"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)