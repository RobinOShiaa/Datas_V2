# Documentation

## Purpose
This class converts weather forecasts from `JSON` data from [Dark Sky API](https://darksky.net/dev) to a `csv` file.

## Important notes
* Everything is in `SI` units, other than `windSpeed` and `windGust`, which are in `km/h`.
* `worldcities.csv` has been edited in the following way: non-state capital cities of China and the United States were removed, because they had too many cities, and the API is limited to 1000 calls/day.
* Original version of `worldcities.csv` is `worldcities_original.csv`.

## Usage
There are two methods: `worldcities_to_dict(countries=None)` and `response_to_csv(coordinates, columns=None)`. The former is necessary to create a dictionary of coordinates for use in the latter method.

* To get the weather data for specific countries, you need to specify this when calling `worldcities_to_dict()`, in the form of an array.
Example:
```python
my_countries = ["ireland", "germany", "croatia"]
my_coordinates = worldcities_to_dict(my_countries)

# Now to get the actual weather data into a csv file
response_to_csv(my_coordinates)
```

* Default countries
```python
countries = ["ireland", "united kingdom", "germany", "france", "united states", "japan", "hong kong", "china"]
```

* You may also specify what columns you wish to use in the csv file instead of the default ones by supplying an array to `response_to_csv()`. Example:
```python
my_countries = ["ireland", "germany", "croatia"]
my_coordinates = worldcities_to_dict(my_countries)

my_columns = ["time", "temperatureMax", "temperatureMin", "pressure"]
response_to_csv(my_coordinates, my_columns)
```

* Default columns
```python
columns = ["time", "temperatureHigh", "temperatureLow", "temperatureMax", "temperatureMin", "pressure", "humidity", "uvIndex",
"windSpeed", "windGust", "precipProbability", "precipType", "precipIntensity", "precipIntensityMax"]
```

## Available columns you may use
```
"time",
"summary",
"icon",
"sunriseTime",
"sunsetTime",
"moonPhase",
"precipIntensity",
"precipIntensityMax",
"precipIntensityMaxTime",
"precipProbability",
"precipType",
"temperatureHigh",
"temperatureHighTime",
"temperatureLow",
"temperatureLowTime",
"apparentTemperatureHigh",
"apparentTemperatureHighTime",
"apparentTemperatureLow",
"apparentTemperatureLowTime",
"dewPoint",
"humidity",
"pressure",
"windSpeed",
"windGust",
"windGustTime",
"windBearing",
"cloudCover",
"uvIndex",
"uvIndexTime",
"visibility",
"ozone",
"temperatureMin",
"temperatureMinTime",
"temperatureMax",
"temperatureMaxTime",
"apparentTemperatureMin",
"apparentTemperatureMinTime",
"apparentTemperatureMax",
"apparentTemperatureMaxTime"
```

## Example code
```python
# You get this key by registering at https://darksky.net/dev
API_KEY = "6820072fb04066296bdfde8adde8f5a9"

# "None" is irrelevant here because that argument is supposed to be a URL, but since this isn't a scraper it doesn't matter (but has to be supplied since the class inherits the Scraper class).
ds_weather = DarkskyWeather("None", API_KEY)

coordinates = ds_weather.worldcities_to_dict(countries=["ireland"])
ds_weather.response_to_csv(coordinates)
```

## Implementation details
Dark Sky `GET` requests require coordinates of places instead of names, in this format: `https://api.darksky.net/forecast/api_key/latitude,longitude`. Therefore I needed an array or dictionary of cities with their coordinates so I could call the API. I found a nice resource on Google in the form of a `csv` file that contains close to 13,000 cities from different countries, including their coordinates. Using this file, `worldcities_to_dict()` creates a dictionary in the following format, which it then returns:
```python
coordinates = {
    "ireland" : [["dublin", 53.3331, -6.2489], ["donegal", 54.6500, -8.1167]],
    "slovakia" : [["bratislava", 48.1500, 17.1170], ["trnava", 48.3666, 17.6000]]
}
```

Even though there are close to 13,000 cities (rows) in `worldcities.csv`, the data gets added to the dictionary instantly even if you wish to append all of the rows. The above dictionary is then used in `response_to_csv()` to perform the actual API calls. The data from each API call is then written to a `csv` file in the form of a row, so each row is written straight to the file (although the file isn't created until execution stops).
