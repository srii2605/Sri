import csv, io, os
from flask import Flask, send_from_directory, jsonify, render_template
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

# Put your CSV URL here (or set env var SHEET_CSV_URL)
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL") or "https://docs.google.com/spreadsheets/d/e/2PACX-1vSyLYmX8qszJmiAE8EJ6c4SMalwe_mEdJqiQJg9eLvBDjUjVtKDdmZzHgFr2Tq7JKnHpMwir8vn0oBj/pub?gid=785015495&single=true&output=csv"

@app.route("/")
def index():
    return render_template("index.html")  # make sure templates/index.html exists

@app.route("/data")
def data():
    try:
        r = requests.get(SHEET_CSV_URL, timeout=15)
        r.raise_for_status()
        f = io.StringIO(r.text)
        reader = csv.DictReader(f)
        rows = list(reader)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/favicon.ico")
def favicon():
    # optional: serve a favicon if you place one at static/favicon.ico
    try:
        return send_from_directory(app.static_folder, "favicon.ico")
    except Exception:
        return ("", 204)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # default 5050
    app.run(host="127.0.0.1", port=port, debug=True)