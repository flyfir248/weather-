from flask import Flask, render_template
import requests
import pandas as pd
import statistics
from geopy.geocoders import Nominatim
import csv

# instantiate a new Nominatim client
app1 = Nominatim(user_agent="firefly")

app = Flask(__name__)

@app.route("/index")
def index():
    with open("result.csv") as file:
        reader = csv.reader(file)
        return render_template("templates/dataframe.html", csv=reader)


def makeavg(df):
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame(
        columns=['Date', 'temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 'apparent_temperature',
                 'precipitation', 'rain', 'showers', 'snowfall', 'snow_depth', 'visibility', 'windspeed_10m',
                 'windspeed_80m', 'winddirection_10m', 'winddirection_80m'])

    x = 0
    y = 24
    row = 0

    # Loop through the data and calculate the average for each section of columns
    while x != 168 or y != 168:
        if y > df.index[-1]:
            break

        date = df['Time'][x].split('T')[0]

        temperature_2m = round(statistics.mean(df[x:y]['temperature_2m']), 3)

        relativehumidity_2m = round(statistics.mean(df[x:y]['relativehumidity_2m']), 3)

        dewpoint_2m = round(statistics.mean(df[x:y]['dewpoint_2m']), 3)

        apparent_temperature = round(statistics.mean(df[x:y]['apparent_temperature']), 3)

        precipitation = round(statistics.mean(df[x:y]['precipitation']), 3)

        rain = round(statistics.mean(df[x:y]['rain']), 3)

        showers = round(statistics.mean(df[x:y]['showers']), 3)

        snow_depth = round(statistics.mean(df[x:y]['snow_depth']), 3)

        snowfall = round(statistics.mean(df[x:y]['snowfall']), 3)

        visibility = round(statistics.mean(df[x:y]['visibility']), 3)

        windspeed_10m = round(statistics.mean(df[x:y]['windspeed_10m']), 3)

        windspeed_80m = round(statistics.mean(df[x:y]['windspeed_80m']), 3)

        winddirection_10m = round(statistics.mean(df[x:y]['winddirection_10m']), 3)

        winddirection_80m = round(statistics.mean(df[x:y]['winddirection_80m']), 3)

        # Store the calculated values in the result DataFrame
        result_df.loc[row] = [date, temperature_2m, relativehumidity_2m, dewpoint_2m, apparent_temperature,
                              precipitation, rain, showers, snowfall, snow_depth, visibility, windspeed_10m,
                              windspeed_80m, winddirection_10m, winddirection_80m]

        x = y + 1
        y = y + 24
        row += 1

    result_df.to_csv('result.csv', index=False)


def get_location(location):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.geocode(location)
    if location is None:
        return None
    return location.latitude, location.longitude


def makedataframe(data):
    # initialize data of lists.
    df = {'Time': data['hourly']['time'],

          'temperature_2m': data['hourly']['temperature_2m'],

          'relativehumidity_2m': data['hourly']['relativehumidity_2m'],

          'dewpoint_2m': data['hourly']['dewpoint_2m'],

          'apparent_temperature': data['hourly']['apparent_temperature'],

          'precipitation': data['hourly']['precipitation'],

          'rain': data['hourly']['rain'],

          'showers': data['hourly']['showers'],

          'snowfall': data['hourly']['snowfall'],

          'snow_depth': data['hourly']['snow_depth'],

          'visibility': data['hourly']['visibility'],

          'windspeed_10m': data['hourly']['windspeed_10m'],

          'windspeed_80m': data['hourly']['windspeed_80m'],

          'winddirection_10m': data['hourly']['winddirection_10m'],

          'winddirection_80m': data['hourly']['winddirection_80m'],

          }

    df = pd.DataFrame(df)
    makeavg(df)


def collect(lat, lon, loc):
    print("The latitude and longitude of", loc, "passed in collect : ", lat, lon)

    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(round(lat, 2)) + "&longitude=" + str(round(lon,2)) + "&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation,rain,showers,snowfall,snow_depth,visibility,windspeed_10m,windspeed_80m,winddirection_10m,winddirection_80m"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data. Status code:", response.status_code)


if __name__ == '__main__':
    loc = input("Enter a location: ")
    lat, lon = get_location(loc)
    a = collect(lat, lon, loc)
    makedataframe(a)
    app.run()
