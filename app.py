from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "a2aaf2d88245d9afbbab7aeedfd94736"

@app.route("/")
def index():
    city = request.args.get("city", "Paris") # si y'a aucune ville on affiche à paris

    if not city:
        return render_template("index.html", city="Unknown", temp="--", description="Enter a city",
                               date="--", time="--", day_or_night="--", temp_feels="--",
                               humidity="--", visibility="--", pressure="--",
                               wind_speed="--", wind_direction="--", wind_deg=0)

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return f"<h3>Weather not found for '{city}'</h3>"

    data = response.json()

    now = datetime.now()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    temp_feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    visibility = data.get("visibility", 0) // 1000
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"]["deg"]
    wind_direction = deg_to_cardinal(wind_deg)

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    day_or_night = "Day" if 6 <= now.hour <= 18 else "Night"

    return render_template("index.html", city=city, temp=temp, description=description,
                           date=date, time=time, day_or_night=day_or_night,
                           temp_feels=temp_feels, humidity=humidity,
                           visibility=visibility, pressure=pressure,
                           wind_speed=wind_speed, wind_direction=wind_direction,
                           wind_deg=wind_deg)

def deg_to_cardinal(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = round(deg / 45) % 8
    return directions[ix]

if __name__ == "__main__":
    app.run(debug=True)
