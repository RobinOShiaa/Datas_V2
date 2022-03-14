from datetime import datetime
from platform import system
import sys
import os


class Scraper:
    
    CSV_FOLDER_PATH = None
    CSV_FILE_NAME = None
    CSV_FILE_PATH = None
    SECONDS = 3
    
    def __init__(self, url=None, CSV_FOLDER_PATH=None):
        self.url = url
        self.CSV_FOLDER_PATH = CSV_FOLDER_PATH

        # If a path has not been supplied. This block of code dynamically generates path for csv folder.
        if self.CSV_FOLDER_PATH is None:
            if system() == "Windows":
                # There is a situation where sys.argv[0] returns a Windows path with forward slashes. Example: C:/Users.
                if "/" in sys.argv[0]:
                    # sys.argv[0] returns path of running script. Not path of base_scraper.py
                    self.CSV_FOLDER_PATH = "\\".join(sys.argv[0].split("/")[:-1]) + "\\csv_files"

                # This else statement is executed if the Windows path is in standard format (i.e. with back slashes).
                else:
                    self.CSV_FOLDER_PATH = "\\".join(sys.argv[0].split("\\")[:-1]) + "\\csv_files"

            # Linux has a different path structure to Windows, so getting the path requires a different method.
            elif system() == "Linux":
                self.CSV_FOLDER_PATH = "/".join(sys.argv[0].split("/")[1:-1]) + "/csv_files"

        # Create folder at CSV_FOLDER_PATH if it doesn't exist.
        try:
            os.makedirs(self.CSV_FOLDER_PATH)
        except FileExistsError:
            # Folder already exists.
            pass

        # Get current datetime for use in generating CSV_FILE_NAME and CSV_FILE_PATH.


        self.CSV_FILE_NAME = current_datetime + ".csv"
        self.CSV_FILE_PATH = self.CSV_FOLDER_PATH + "\\" + self.CSV_FILE_NAME

    def scrape(self):
        """Returns a csv file."""
        pass
