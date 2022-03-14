from scraper_classes.base_scraper import Scraper
from bs4 import BeautifulSoup
import requests


class Bs4Scraper(Scraper):

    def __init__(self, url=None, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        if self.url is not None:
            self.result = requests.get(self.url)
            self.soup = BeautifulSoup(self.result.content, "lxml")
