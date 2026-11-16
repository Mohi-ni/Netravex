import os
import random
import json
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/api/scoping-call", methods=["POST"])
def create_scoping_inquiry():
    data = request.get_json()
    
    if not data or not data.get("consent"):
        return jsonify({"error": "DPDP consent and required fields must be provided."}), 400

    ref_id = f"NVX-{random.randint(10000, 99999)}"

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scoping_inquiries 
            (reference_id, full_name, organization_name, work_email, phone_number, readiness_score, checked_items, consent_given)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ref_id,
            data.get("fullName"),
            data.get("organization"),
            data.get("email"),
            data.get("phone"),
            data.get("readinessScore", 0),
            json.dumps(data.get("checkedItems", [])),
            True
        ))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"success": True, "referenceId": ref_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)