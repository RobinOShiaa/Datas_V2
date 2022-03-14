from scraper_classes.urllib_scraper import UrllibScraper
from scrapers.logger import get_logger
from datetime import datetime
from sys import exit
import urllib.request
import json
import csv


class DarkskyWeather(UrllibScraper):
    """This class uses an API instead of scraping. However Scraper() is used for convenience (path, name).
    This script is supposed to replace the 'accuweather' scraper because accuweather blocked me from scraping, and an
    API is more efficient.

    Dark Sky API is used, and allows for up to 1000 calls per day for free."""

    logger = get_logger("DarkskyWeather")

    def __init__(self, url=None, CSV_FOLDER_PATH=None, API_KEY="6820072fb04066296bdfde8adde8f5a9"):
        super().__init__(url, CSV_FOLDER_PATH)
        self.API_KEY = API_KEY
        self.logger.info("Starting")

    # https://darksky.net/dev/docs
    def response_to_csv(self, coordinates, columns=None):
        """Method creates a csv file from request.get() API calls."""

        # If a user hasn't specified any columns, use default ones.
        if columns is None:
            columns = ["time", "temperatureHigh", "temperatureLow", "temperatureMax", "temperatureMin", "pressure",
                       "humidity", "uvIndex", "windSpeed", "windGust", "precipProbability", "precipType",
                       "precipIntensity", "precipIntensityMax"]

        # Creating csv file at CSV_FILE_PATH and writing to it row by row.
        with open(self.CSV_FILE_PATH, "w+", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)

            # Write the column names first.
            writer.writerow(["country", "city"] + columns)

            # Looping through all of the cities in all countries.
            for country in coordinates:
                for city in coordinates[country]:
                    print(country.title() + ", " + city[0].title())

                    # City coordinates
                    lat = city[1]
                    lng = city[2]

                    # Call the Dark Sky API. A few queries can be set after the question mark.
                    response = urllib.request.urlopen(
                        "https://api.darksky.net/forecast/{}/{},{}?units=ca&exclude=currently,"
                        "minutely,hourly,alerts,flags".format(self.API_KEY, lat, lng))

                    try:
                        # 8 elements (days) in the following list. [0] seems to be a day behind, so [1] is used.
                        daily_forecast = json.load(response)["daily"]["data"][1]
                    except SyntaxError as e:
                        self.logger.error("Error: ", str(e))
                        self.logger.info("\nDaily API usage limit reached.\nStopping...")
                        exit()

                    # This list is 1 row in the csv file. City & country not in columns, so added manually.
                    tmp_lst = [country, city[0]]

                    # Looping through weather forecast for current city.
                    for key in columns:
                        if "time" in key.lower():
                            time = datetime.utcfromtimestamp(daily_forecast[key]).strftime("%Y-%m-%d %H:%M:%S")
                            tmp_lst.append(time)
                        else:
                            # If a value is missing catch it, and call it "none".
                            try:
                                tmp_lst.append(daily_forecast[key])
                            except KeyError:
                                tmp_lst.append("none")
                    writer.writerow(tmp_lst)
        self.logger.info("Finished")

    def worldcities_to_dict(self, countries=None):
        """Method returns a dictionary containing countries, cities, latitudes, and longitudes. These are necessary
        for working with the Dark Sky API."""

        if countries is None:
            countries = ["ireland", "united kingdom", "germany", "france", "united states", "japan", "hong kong", "china"]

        database = {}
        with open("worldcities.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            # Skip header row
            next(reader)

            # row = ['city', 'city_ascii', 'lat', 'lng', 'country', 'iso2', 'iso3', 'admin_name', 'capital',
            # 'population', 'id']
            for row in reader:
                country = row[4].lower()
                city = row[1].lower()
                lat = float(row[2])
                lng = float(row[3])

                # {"country" : [["city_ascii", lat, lng]]}
                if country in countries:
                    if country in database.keys():
                        database[country] += [[city, lat, lng]]
                    else:
                        database[country] = [[city, lat, lng]]
        return database


if __name__ == "__main__":
    DarkskyWeather().scrape()
