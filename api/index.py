from flask import Flask, render_template, request, abort
import requests
from datetime import datetime, timezone

app = Flask(__name__)
api_key = "a2aaf2d88245d9afbbab7aeedfd94736"


def kelvin_to_celsius(deg):
    return deg - 273.15


def cardinal_direction(angle):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    # On divise l'angle par 22.5 car chaque direction est tt les 22.5 deg dcp ça donne la direction cardinale
    return directions[round(angle / 22.5) % 16]


def get_coordinates(location):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={api_key}"
    response = requests.get(url)
    return response.json()[0]


def get_weather_data(city):
    location_data = get_coordinates(city)
    lat, lon = location_data["lat"], location_data["lon"]
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    return response.json()


@app.route('/')
def index():
    city = request.args.get("city")
    if city is None:
        abort(400, 'Missing argument city')

    data = get_weather_data(city)

    dt_object = datetime.fromtimestamp(data["dt"], timezone.utc)
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], timezone.utc).hour
    sunset = datetime.fromtimestamp(data["sys"]["sunset"], timezone.utc).hour
    hour = dt_object.hour

    # Left part information
    temp = round(kelvin_to_celsius(data["main"]["temp"]), 1)
    description = data["weather"][0]["main"]
    date = dt_object.strftime("%d-%B-%Y")
    time = dt_object.strftime("%A, %H:%M")
    day_or_night = "Day" if sunrise < hour < sunset else "Night"
    city = data["name"]

    # Right part information
    temp_feels = round(kelvin_to_celsius(data["main"]["feels_like"]), 1)
    visibility = round(data["visibility"] / 1000, 2)
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"]["deg"]
    wind_direction = cardinal_direction(wind_deg)

    return render_template("index.html",
                           temp=temp,
                           description=description,
                           date=date,
                           time=time,
                           day_or_night=day_or_night,
                           city=city,
                           temp_feels=temp_feels,
                           humidity=humidity,
                           visibility=visibility,
                           pressure=pressure,
                           wind_speed=wind_speed,
                           wind_deg=wind_deg,
                           wind_direction=wind_direction
                           )


if __name__ == '__main__':
    app.run()
