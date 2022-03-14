from scraper_classes.base_scraper import Scraper


class UrllibScraper(Scraper):

    def __init__(self, url=None, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
