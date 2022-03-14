from scraper_classes.base_scraper import Scraper
from selenium import webdriver
from sys import exit
from os import environ


class ChromeScraper(Scraper):

    def __init__(self, url=None, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

        try:
            self.CHROME_DRIVER_PATH = \
                [cd_path for cd_path in environ.get("PATH").split(":") if "chromedriver" in cd_path][0]
        except IndexError:
            # IndexError occurs when "chromedriver.exe" is not found.
            print("chromedriver.exe not in path")
            exit()

        # Changing download directory to csv_folder
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": self.CSV_FOLDER_PATH,
                                                  "plugins.always_open_pdf_externally": True})

        self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH, chrome_options=options)
