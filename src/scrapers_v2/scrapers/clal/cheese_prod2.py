from scraper_classes.chrome_scraper import ChromeScraper
import csv


class Clal_Cheese2(ChromeScraper):

    def __init__(self,url=('https://www.clal.it/en/?section=burro_francia%22,%22http://www.clal.it/en/index.php?section=poudre'),CSV_FOLDER_PATH=None):
     super().__init__(url,CSV_FOLDER_PATH)
     self.driver.get(url)
     self.Data = []

    def scrape(self):
        data = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[11]/tbody/tr')][1:]
        print(data)
        titles = data[0].strip().split(' ')

        print(titles)
        details = data[1].strip().split('*')
        print(details)
        i = 2

        while i < len(data):
            td = data[i].split()
            self.Data.append(td)
            i+=1

        print(self.Data)
        self.to_csv(titles,details)

    def to_csv(self,titles,details):
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(titles)
            writer.writerow(details)
            for j in self.Data:
                writer.writerow(j)


if __name__ == "__main__":
    Clal_Cheese2().scrape()
