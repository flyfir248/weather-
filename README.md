## Weather Forecast Web App
This web app displays the weather forecast data for a given location, as well as some basic statistics about the weather data. The app is built using Flask and it makes use of the Open Meteo API to retrieve the weather forecast data.

### Installation
To run the application, you need to have the following packages installed:

1.) Flask

2.) requests

3.) pandas

4.) statistics

5.) geopy

To install the packages, use the following command:

```
pip install Flask requests pandas statistics geopy
```

### Usage
To use the application, run the app.py file using the following command:

```
python app.py
```

Once the app is running, you can access it by opening a web browser and navigating to http://localhost:5000.

To retrieve the weather forecast data for a location, enter the location in the search bar and click the "Search" button. The app will retrieve the latitude and longitude of the location using the **geopy** package, and then use the Open Meteo API to retrieve the weather forecast data for that location.

The app will display a table with the weather data, as well as some basic statistics about the weather data. The statistics are calculated using the statistics package.

#### Files
- app.py - the main Flask application file
- templates folder - contains the HTML templates used by the app
- result.csv - contains the processed weather data

#### Limitations
The app retrieves the weather data for the current day only.
The app can only retrieve weather data for locations with latitude and longitude coordinates.