# app.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
# Allow CORS for all origins, adjust in production for security
CORS(app)

# MongoDB Configuration
MONGO_DB_CONNECTION_STRING = os.getenv("MONGO_DB_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_DB_CONNECTION_STRING or not MONGO_DB_NAME:
    print("Error: MongoDB connection string or database name not set in .env")
    exit(1)

try:
    client = MongoClient(MONGO_DB_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    estimates_collection = db["estimates"]
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# OLAMA Configuration
OLAMA_API_URL = os.getenv("OLAMA_API_URL")
OLAMA_MODEL_NAME = os.getenv("OLAMA_MODEL_NAME")

if not OLAMA_API_URL or not OLAMA_MODEL_NAME:
    print("Error: OLAMA API URL or model name not set in .env")
    exit(1)

def get_olama_estimate(requirements_text):
    """Sends requirements to the local OLAMA server and returns the response."""
    prompt = f"""
    Based on the following software project requirements, provide an estimate for:
    1.  **Total Estimated Cost (USD)**: Provide a single numerical value (e.g., $50,000).
    2.  **Agile Development Estimate**: Provide the duration in weeks or months (e.g., 12 weeks, 3 months).
    3.  **Waterfall Development Estimate**: Provide the duration in weeks or months (e.g., 20 weeks, 5 months).

    Present the output clearly with labels. If a value cannot be determined, state "N/A".

    Project Requirements:
    {requirements_text}
    """

    payload = {
        "model": OLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response from OLAMA.")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with OLAMA: {e}")
        return f"Error: Could not connect to OLAMA server. Details: {e}"
    except Exception as e:
        print(f"Unexpected error during OLAMA interaction: {e}")
        return f"Error: An unexpected error occurred: {e}"

@app.route('/estimate', methods=['POST'])
def estimate_project():
    """Endpoint for getting project estimates."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.json
    project_name = data.get('projectName', 'Untitled Project')
    requirements_text = f"""
    Project Name: {project_name}
    Description: {data.get('description', '')}
    Key Features: {data.get('features', '')}
    Technologies: {data.get('technologies', '')}
    Notes: {data.get('notes', '')}
    """

    print(f"Processing estimate for: {project_name}")
    olama_response = get_olama_estimate(requirements_text)

    # Parse response
    cost = "N/A"
    agile = "N/A"
    waterfall = "N/A"
    
    for line in olama_response.split('\n'):
        if "Total Estimated Cost (USD):" in line:
            cost = line.split(":")[-1].strip()
        elif "Agile Development Estimate:" in line:
            agile = line.split(":")[-1].strip()
        elif "Waterfall Development Estimate:" in line:
            waterfall = line.split(":")[-1].strip()

    # Save to MongoDB
    try:
        estimates_collection.insert_one({
            "timestamp": datetime.datetime.now(),
            "projectName": project_name,
            "costEstimate": cost,
            "agileEstimate": agile,
            "waterfallEstimate": waterfall,
            "rawResponse": olama_response
        })
    except Exception as e:
        print(f"Database save error: {e}")

    return jsonify({
        "projectName": project_name,
        "costEstimate": cost,
        "agileEstimate": agile,
        "waterfallEstimate": waterfall,
        "rawResponse": olama_response
    })

@app.route('/history', methods=['GET'])
def get_history():
    """Retrieves estimation history."""
    try:
        records = list(estimates_collection.find().sort("timestamp", -1).limit(20))
        for r in records:
            r['_id'] = str(r['_id'])
            r['timestamp'] = r['timestamp'].isoformat()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    """Serve the frontend."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)