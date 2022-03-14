

import urllib.request as url
import zipfile
from datetime import datetime

from scraper_classes.chrome_scraper import ChromeScraper



class gdelt(ChromeScraper):



    def __init__(self, url = ('http://data.gdeltproject.org/events/index.html'), CSV_FOLDER_PATH=None):
     super().__init__(url, CSV_FOLDER_PATH)
     self.driver.get(url)
     print('Start scraping at %s...' % datetime.now())




    def download(self):
        t = self.driver.find_elements_by_xpath('/html/body/ul/li/a')
        links = [i for i in t[3:]]
        for i in links:
            url.urlopen(i.get_attribute('href'))
            with zipfile.ZipFile('./csv_files/'+i.text, "r") as z:
                z.extractall(self.CSV_FOLDER_PATH)

    print('finished at %s...' % datetime.now())





if __name__ == "__main__":
    gdelt().download()
