from scraper_classes.base_scraper import Scraper
from selenium import webdriver
from sys import exit
import os


class FirefoxScraper(Scraper):

    def __init__(self, url=None, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

        try:
            self.GECKO_DRIVER_PATH = \
                [path for path in os.environ["PATH"].split(";") if "geckodriver" in path][0]
        except IndexError:
            # IndexError occurs when "geckodriver" is not found.
            print("geckodriver not in path")
            exit()

        # Changing download directory to csv_files folder & disabling dialogue window
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.preferences.instantApply", True)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", self.CSV_FOLDER_PATH)

        self.driver = webdriver.Firefox(executable_path=self.GECKO_DRIVER_PATH, firefox_profile=profile)
