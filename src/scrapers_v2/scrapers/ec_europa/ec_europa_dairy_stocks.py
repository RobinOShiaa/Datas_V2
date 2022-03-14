from scraper_classes.chrome_scraper import ChromeScraper
import csv
import time
import os
from scrapers import logger
from tika import parser
import re
class EcEuropaStocks(ChromeScraper):
    ec_logger = logger.get_logger("ec europa_logger")
    def __init__(self, url = 'https://ec.europa.eu/agriculture/sites/agriculture/files/market-observatory/milk/pdf/eu-milk-internal-measures-stocks_en.pdf',
                 CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        '#open url to pdf'
        self.ec_logger.info('Start scraping')
        self.driver.get(self.url)
        time.sleep(3)

        '#open downloaded pdf, save to raw and delete from folder'
        raw = parser.from_file('csv_files/eu-milk-internal-measures-stocks_en.pdf')
        os.remove(self.CSV_FOLDER_PATH + "/eu-milk-internal-measures-stocks_en.pdf")
        start_index = raw['content'].index("Page - 7 -") + len("Page - 7 -")
        raw = raw["content"][start_index: - 14]

        '#seperating into rows'
        text = os.linesep.join([s for s in raw.splitlines() if s])
        s = re.sub(r'(?<=\d)\s+(?=\d)', ',', text)
        split_up = (s.splitlines())
        print(split_up)

        '#Change spaces to commas for csv format'
        split_up[2] = 'Months,' + split_up[2].replace(' ', ',')
        i = 4
        j = 0
        final_list = []

        '#first while loop appends titles to final_list and the second loop adds commas between title/numbers'
        while j < 4:
            final_list.append(split_up[j])
            j += 1
        while i < len(split_up):
            b = re.sub(r'(?<=\b)\s+(?=\d)', ',', split_up[i])
            final_list.append(b)
            i += 1
        print(final_list)

        '#Begin writing to csv and split each line by ,'
        with open(self.CSV_FOLDER_PATH + '/ec_europa_dairy_stocks.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
            for row in final_list:
                writer.writerow(row.split(','))

#EcEuropaStocks().scrape()