from app import app
from flask import request, jsonify, abort
import requests
import os


@app.route("/v1/current/")
def get_current():
    url = os.getenv("weather_url")
    city = request.args.get("city")
    if city is None:
        return abort(403)

    params = {
        "q": city,
        "APPID": os.getenv("OpenWeather")
    }
    temp = requests.get(url, params=params).json()["main"]["temp"] - 273.15

    response = {
        "city": city,
        "unit": "celsius",
        "temperature": round(temp, 2)
    }
    return jsonify(response)


@app.route("/v1/forecast/")
def get_forecast():
    url = os.getenv("forecast_url")
    city = request.args.get("city")
    dt = request.args.get("dt")
    params = {
        "q": city,
        "APPID": os.getenv("OpenWeather")
    }
    data = requests.get(url, params=params).json()["list"]

    if dt is None:
        return jsonify(data)

    dt = int(dt)
    if dt < data[0]["dt"] or dt > data[-1]["dt"]:
        return abort(403)

    for idx in range(len(data) - 2):
        if dt >= data[idx]["dt"] and dt <= data[idx + 1]["dt"]:
            if dt - data[idx]["dt"] < data[idx + 1]["dt"] - dt:
                temp = data[idx]["main"]["temp"] - 273.15
            else:
                temp = data[idx + 1]["main"]["temp"] - 273.15

    response = {
        "city": city,
        "unit": "celsius",
        "temperature": round(temp, 2)
    }
    return jsonify(response)
