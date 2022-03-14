from scrapers.darksky_weather.weather import DarkskyWeather
import unittest
import os


class TestDarkskyWeather(unittest.TestCase):

    # Initialise a DarkskyWeather object
    ds_weather = DarkskyWeather(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))

    def test_worldcities_to_dict(self):
        d = self.ds_weather.worldcities_to_dict(countries=["croatia"]).values()
        # Have to iterate once because values() is nested. d = { "country": [[city1], [city2], [city3]] }
        for x in d:
            # Croatia (in worldcities.csv) has 21 cities (so len == 21).
            assert len(x) == 21

    def test_response_to_csv(self):
        columns = ["time", "temperatureMax", "temperatureMin", "pressure"]

        countries = ["united states", "china", "ireland", "slovakia"]

        coordinates = self.ds_weather.worldcities_to_dict(countries)
        self.ds_weather.response_to_csv(coordinates)

        assert os.path.exists(self.ds_weather.CSV_FILE_PATH) is True


if __name__ == "__main__":
    unittest.main()
