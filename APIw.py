from flask import Flask, request, render_template
import requests

app = Flask(__name__)

api_key = '9904dc54d2a25f3b7a21b3bf6f349535'


def fahrenheit_to_celsius(temp):
    return round((temp - 32) * 5 / 9, 2)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form.get('cityName')

        if not city:
            return render_template('index.html', error="City name is required.")

        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
        )

        if weather_data.json().get('cod') == '404':
            return render_template('index.html', error="City not found.")

        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        icon_code = weather_data.json()['weather'][0]['icon']
        temp_celsius = fahrenheit_to_celsius(temp)

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

        return render_template('index.html', city=city, weather=weather, icon_url=icon_url, temp_c=temp_celsius)

    return render_template('index.html')


if __name__ == '__main__':
    app.run( debug=True)
