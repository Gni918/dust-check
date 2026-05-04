from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "d20f7980935291dfada00ffe37d740017f30266838299b6134eaacf66fcaedf8"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/dust")
def dust():
    station = request.args.get("station", "중구")

    url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"

    params = {
        "serviceKey": API_KEY,
        "returnType": "json",
        "numOfRows": "100",
        "pageNo": "1",
        "sidoName": "인천",
        "ver": "1.0"
    }

    response = requests.get(url, params=params)
    response.encoding = "utf-8"
    data = response.json()

    items = data["response"]["body"]["items"]

    selected = None

    for item in items:
        if item.get("stationName") == station:
            selected = item
            break

    if selected is None:
        return jsonify({
            "error": "선택한 측정소를 찾을 수 없습니다.",
            "station": station
        })

    return jsonify({
        "stationName": selected.get("stationName"),
        "pm10": selected.get("pm10Value"),
        "pm25": selected.get("pm25Value"),
        "pm10Grade": selected.get("pm10Grade"),
        "pm25Grade": selected.get("pm25Grade"),
        "dataTime": selected.get("dataTime")
    })

if __name__ == "__main__":
    app.run(debug=True)
