"""
app.py — Flask application entry point
Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, render_template, jsonify, request
from model import run_all, run_analysis, CONFIGS, COMPANIES

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    """
    Return full simulation results as JSON.
    Query params:
      risk_life — float, GPU depreciation life in years (default 6.0)
      method    — str,   "SL" or "DDB"                 (default "SL")

    Note: energy_rate (0.05) and growth_rate (12%) are hardcoded in the model.
    """
    risk_life = float(request.args.get("risk_life", 6.0))
    method    = request.args.get("method", "SL")

    data = run_all(risk_life, method)

    # Year-3 comparison between DDB and SL for the comparison chart
    ddb_year3 = {co: run_analysis(co, risk_life, "DDB")[2]["depr"] for co in COMPANIES}
    sl_year3  = {co: run_analysis(co, risk_life, "SL")[2]["depr"]  for co in COMPANIES}

    return jsonify({
        "data":      data,
        "ddb_year3": ddb_year3,
        "sl_year3":  sl_year3,
        "configs":   CONFIGS,
        "companies": COMPANIES,
    })


if __name__ == "__main__":
    app.run(debug=True)
