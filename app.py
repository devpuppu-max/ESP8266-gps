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

        button {
            padding: 12px 18px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            background: black;
            color: white;
        }
    </style>
</head>

<body>

<div class="box">

    <h2>ESP8266 Location</h2>

    <p>Latitude:
        <span id="lat">Waiting...</span>
    </p>

    <p>Longitude:
        <span id="lng">Waiting...</span>
    </p>

    <p>Accuracy:
        <span id="accuracy">Waiting...</span>
    </p>

    <p>Last update:
        <span id="time">Waiting...</span>
    </p>

    <button onclick="openMap()">
        Open Map
    </button>

</div>


<script>

let latitude = null;
let longitude = null;


// Get newest location
async function updateLocation() {

    try {

        const response =
            await fetch("/location?time=" + Date.now());

        const data =
            await response.json();


        if (data.lat != null) {

            latitude = data.lat;
            longitude = data.lng;

            document.getElementById("lat").innerText =
                data.lat;

            document.getElementById("lng").innerText =
                data.lng;

            document.getElementById("accuracy").innerText =
                data.accuracy + " m";

            document.getElementById("time").innerText =
                data.time;
        }

    }

    catch(error) {

        console.log(error);

    }
}


// Update every 2 seconds
setInterval(updateLocation, 2000);


// Get immediately
updateLocation();


// Update when returning to page
window.addEventListener("pageshow", function() {
    updateLocation();
});


function openMap() {

    if (latitude == null) {
        alert("Location not received yet");
        return;
    }

    const url =
        "https://www.openstreetmap.org/?mlat="
        + latitude
        + "&mlon="
        + longitude
        + "#map=17/"
        + latitude
        + "/"
        + longitude;

    window.open(url, "_blank");
}

</script>

</body>
</html>
""")


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

    response = jsonify(latest)

    # Prevent browser caching
    response.headers["Cache-Control"] = \
        "no-store, no-cache, must-revalidate, max-age=0"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)    
