
from datetime import datetime
from scraper_classes.chrome_scraper import ChromeScraper



class trade_api(ChromeScraper):

    def __init__(self,url,CSV_FOLDER_PATH = None):
        super().__init__(url,CSV_FOLDER_PATH)
        self.driver.get(url)
        self.urls = []
        self.Data = []
        self.memo = {}
        print('Start scraping at %s...' % datetime.now())


t = trade_api('http://api.census.gov/data/timeseries/intltrade/exports?get=usda&key=9a398381359d637f63bc98a674667714fe75e04d&year=2016&month=01')