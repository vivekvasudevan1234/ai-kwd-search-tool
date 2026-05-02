from flask import Flask, render_template, request, jsonify, send_from_directory
import os

from tools.country_rates import COUNTRY_RATES
from tools.calculate_ai_volume import estimate_ai_volume

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route("/")
def index():
    countries = sorted(COUNTRY_RATES.keys())
    return render_template("index.html", countries=countries)


@app.route("/estimate", methods=["POST"])
def estimate():
    body = request.get_json(force=True)
    keyword = (body.get("keyword") or "").strip()
    country = (body.get("country") or "").strip()
    kw_volume = body.get("kw_volume")
    relative_diff = body.get("relative_diff")

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    if country not in COUNTRY_RATES:
        return jsonify({"error": f"Unknown country: {country}"}), 400
    if kw_volume is None:
        return jsonify({"error": "Monthly search volume is required"}), 400
    if relative_diff is None:
        return jsonify({"error": "Relative usage difference is required"}), 400

    try:
        kw_volume = int(kw_volume)
    except (TypeError, ValueError):
        return jsonify({"error": "Monthly search volume must be a whole number"}), 400

    try:
        relative_diff = float(relative_diff)
    except (TypeError, ValueError):
        return jsonify({"error": "Relative usage difference must be a number"}), 400

    rates = COUNTRY_RATES[country]
    base_rate = rates["base_rate"]
    avg_ai_market_use = rates["avg_ai_market_use"]

    estimated = estimate_ai_volume(kw_volume, base_rate, relative_diff, avg_ai_market_use)

    return jsonify({
        "keyword": keyword,
        "country": country,
        "kw_volume": kw_volume,
        "base_rate": base_rate,
        "avg_ai_market_use": avg_ai_market_use,
        "relative_diff": relative_diff,
        "estimated_ai_volume": round(estimated),
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
