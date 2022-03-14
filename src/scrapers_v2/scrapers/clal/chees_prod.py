from scraper_classes.bs4_scraper import Bs4Scraper
import csv


class Clal_Cheese(Bs4Scraper):

    def __init__(self, url=('https://www.clal.it/en/index.php?section=produzioni_cheese'), CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

    def scrape(self):
        el = self.soup.find("table", {"class": "quadro"})
        a = [i.find_all("td") for i in el.find_all("tr")]
        with open(self.CSV_FILE_PATH, "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([tag.text for tag in a[0]])
            for row in a[1:-2]:
                writer.writerow([tag.text for tag in row])


if __name__ == "__main__":
    Clal_Cheese().scrape()
