from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        try:
            geolocator = Nominatim(user_agent="weather-app")
            location = geolocator.geocode(city)
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
            local_time = datetime.now(pytz.timezone(timezone))
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a03f2328b30c709ec7fd4e34f6ee0f9d"
            data = requests.get(url).json()
            weather = {
                'city': city,
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'temp': int(data['main']['temp'] - 273.15),
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'time': local_time.strftime("%I:%M %p")
            }
        except:
            weather = None
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
