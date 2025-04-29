from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, ASCENDING
import requests

app = Flask(__name__)
CORS(app)

# ─────────────────  MongoDB  ─────────────────
client = MongoClient("mongodb://localhost:27017")
db = client["matcher"]
collection = db["selected_matches"]

# Unique on (query, filename, amount)
collection.create_index(
    [("query", ASCENDING), ("filename", ASCENDING), ("amount", ASCENDING)], unique=True
)

# ────────────────  External APIs  ────────────────
EXTRACT_URL = "https://plankton-app-qajlk.ondigitalocean.app/extraction_api"
MATCH_URL = "https://endeavor-interview-api-gzwki.ondigitalocean.app/match"


# ─────────────────────  Routes  ─────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]

    # 1️⃣ Extract
    files = {"file": (f.filename, f.stream, f.mimetype or "application/pdf")}
    ext_resp = requests.post(EXTRACT_URL, files=files)
    ext_resp.raise_for_status()
    extracted = ext_resp.json()  # list[dict]

    # 2️⃣ Batch-match
    queries = [d["Request Item"] for d in extracted if d.get("Request Item")]
    if not queries:
        return jsonify({"error": "no request items"}), 400

    batch = requests.post(MATCH_URL + "/batch", json={"queries": queries}).json()
    results_map = batch["results"]

    # 3️⃣ Combine
    combined = {}
    for d in extracted:
        q = d.get("Request Item")
        if not q:
            continue
        combined[q] = {
            "matches": results_map.get(q, []),
            "amount": d.get("Amount"),
            "unit_price": d.get("Unit Price"),
            "total": d.get("Total"),
        }
    return jsonify(combined)


@app.route("/search-match", methods=["GET"])
def search_match():
    query = request.args.get("query", "")
    limit = request.args.get("limit", 1)
    if not query:
        return jsonify({"results": []})
    try:
        resp = requests.get(MATCH_URL, params={"query": query, "limit": limit})
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/select-best", methods=["POST"])
def select_best():
    data = request.get_json()
    required = ("query", "filename", "amount", "best_match")
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400

    collection.update_one(
        {
            "query": data["query"],
            "filename": data["filename"],
            "amount": data["amount"],
        },
        {
            "$set": {
                "best_match": data["best_match"],
                "unit_price": data.get("unit_price"),
                "total": data.get("total"),
            }
        },
        upsert=True,
    )
    return jsonify({"status": "saved"})


@app.route("/selected")
def selected():
    return jsonify(list(collection.find({}, {"_id": 0})))


@app.route("/delete", methods=["POST"])
def delete_one():
    data = request.get_json()
    required = ("query", "filename", "amount")
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400
    collection.delete_one(
        {
            "query": data["query"],
            "filename": data["filename"],
            "amount": data["amount"],
        }
    )
    return jsonify({"status": "deleted"})


@app.route("/delete-all", methods=["POST"])
def delete_all():
    collection.delete_many({})
    return jsonify({"status": "all deleted"})


# ────────────────────  Main  ────────────────────
if __name__ == "__main__":
    print("✅  Flask running on http://localhost:5000")
    app.run(debug=True)
