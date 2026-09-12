from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

latest = {
    "lat": None,
    "lng": None,
    "accuracy": None,
    "time": None
}

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP8266 Location</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="5">
        <style>
            body {
                font-family: Arial;
                text-align: center;
                margin-top: 40px;
            }
            .box {
                display: inline-block;
                padding: 25px;
                border: 1px solid #aaa;
                border-radius: 12px;
            }
            a {
                display: inline-block;
                margin-top: 15px;
                padding: 10px 15px;
                background: #222;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h2>ESP8266 Location</h2>

            {% if lat %}
                <p>Latitude: {{ lat }}</p>
                <p>Longitude: {{ lng }}</p>
                <p>Accuracy: {{ accuracy }} m</p>
                <p>Last update: {{ time }}</p>

                <a href="https://www.openstreetmap.org/?mlat={{lat}}&mlon={{lng}}#map=17/{{lat}}/{{lng}}">
                    Open Map
                </a>
            {% else %}
                <p>No location received yet.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """,
    lat=latest["lat"],
    lng=latest["lng"],
    accuracy=latest["accuracy"],
    time=latest["time"])

@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error"}), 400

    latest["lat"] = data.get("lat")
    latest["lng"] = data.get("lng")
    latest["accuracy"] = data.get("accuracy")
    latest["time"] = datetime.now().strftime("%H:%M:%S")

    return jsonify({"status": "ok"})

@app.route("/location")
def location():
    return jsonify(latest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
