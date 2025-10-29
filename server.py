
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")  # e.g. https://your-frontend.web.app
MONGO_URI = "mongodb+srv://priyanka_db_user:echo2025@userinfo.bzjqkz1.mongodb.net/" # mongodb+srv://user:URL_ENCODED_PASS@cluster.mongodb.net/
MONGO_DB =  "ECHO"
MONGO_COLL = "userinfo"

# Safer CORS: only allow your frontend to hit /api/*
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_ORIGIN]}})

# Connect & ping Atlas (fail fast if IP/creds wrong)
client = None
reports_collection = None
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db = client[MONGO_DB]
    reports_collection = db[MONGO_COLL]
    print("✅ Connected to MongoDB Atlas.")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

def oid(x): return str(x) if isinstance(x, ObjectId) else x

@app.route("/api/reports", methods=["POST"])
def save_report():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid or empty JSON"}), 400
    if reports_collection is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 500

    data.setdefault("createdAt", datetime.utcnow())
    try:
        res = reports_collection.insert_one(data)
        return jsonify({"status": "success", "id": oid(res.inserted_id)}), 201
    except Exception as e:
        print(f"❌ Insert error: {e}")
        return jsonify({"status": "error", "message": "DB write failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=int(os.getenv("PORT", "8080")))
