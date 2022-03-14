from scraper_classes.base_scraper import Scraper
from scrapers.logger import get_logger
from datetime import datetime
import pandas as pd


class Usda(Scraper):

    logger = get_logger("Usda")
    api_urls = {
        "all_animal_products": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&agg_level_desc=NATIONAL&freq_desc=WEEKLY",
        "dairy_quickstats": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=DAIRY&agg_level_desc=NATIONAL&freq_desc=MONTHLY",
        "dairy_quickstats_cold_storage": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&commodity_desc=BUTTER&short_desc=BUTTER%2C%20COLD%20STORAGE%20-%20STOCKS%2C%20MEASURED%20IN%20LB",
        "hog_slaughters": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=LIVESTOCK&commodity_desc=HOGS&statisticcat_desc=SLAUGHTERED",
        "pig_crops": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=LIVESTOCK&commodity_desc=HOGS&statisticcat_desc=PIG%20CROP&freq_desc=MONTHLY",
        "pork_production_stocks": "http://quickstats.nass.usda.gov/api/api_GET/?key=872CA637-FC03-33B0-8917-3E1972173A4A&format=CSV&source_desc=SURVEY&sector_desc=ANIMALS%20%26%20PRODUCTS&group_desc=LIVESTOCK&commodity_desc=PORK"
    }

    def scrape(self, desired_stats=None, year_range=None):
        # Check for invalid input
        current_year = datetime.now().year
        if self.is_valid_year_range(year_range, current_year) is False:
            return self.logger.error("Invalid year range. Accepted range: [1915, current year]")

        # If no year_range is supplied, update it to rage(1915, current year)
        year_range_ = range(1915, current_year + 1)  # range is last element exclusive
        if year_range is None:
            year_range = year_range_

        # If no desired_stats are supplied, update it to the list of api_urls keys
        if desired_stats is None:
            desired_stats = list(self.api_urls.keys())
        elif not set(desired_stats).issubset(set(list(self.api_urls.keys()))):
            # Invalid input
            return self.logger.error("Invalid desired_stats")

        # Loop through api_urls
        for url in self.api_urls.items():
            if url[0] in desired_stats:
                all_data = []
                # Loop through range of years in reverse order & append data as a DataFrame to all_data
                for year in range(year_range[0], year_range[1] + 1)[::-1]:
                    self.logger.info("Downloading {}".format(url[0] + "_" + str(year)))
                    all_data.append(pd.read_csv(url[1] + "&year={}".format(year), index_col=False))

                # Concatenate all_data to one DataFrame & write to csv file
                self.logger.info("Writing data to file")
                df = pd.concat(all_data, axis=0, ignore_index=True)
                df.to_csv(self.CSV_FOLDER_PATH + "\\" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_" + url[0] +
                          "_{}-{}".format(year_range[0], year_range[1]) + ".csv", index=None)
        self.logger.info("Finished")

    def is_valid_year_range(self, year_range, current_year):
        """Method checks whether the year_range is valid. Needs to be a list in this format: [1915, 2019]"""
        if len(year_range) == 2:
            try:
                int(year_range[0])
                int(year_range[1])
            except (TypeError, ValueError):
                # Range is not int
                return False
            if (year_range[1] <= current_year) and (year_range[0] <= year_range[1]) and (year_range[0] >= 1915):
                return True
        return False


if __name__ == "__main__":
    Usda().scrape()
