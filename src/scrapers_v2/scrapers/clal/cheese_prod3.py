from scraper_classes.chrome_scraper import ChromeScraper
import csv


class Clal_Cheese3(ChromeScraper):

    def __init__(self,url=('https://www.clal.it/en/index.php?section=produzioni_chees'),CSV_FOLDER_PATH=None):
        super().__init__(url,CSV_FOLDER_PATH)
        self.driver.get(url)
        self.Data = []
        self.d = {}

    def scrape(self):
        Headers = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr[1]/td')][1:]
        print(Headers)
        Header = [self.driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr[2]/td').text]
        Col1 = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr/td/a')]
        Col1_names = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr/td//b') if '-' not in i.text and '+' not in i.text and i.text != '0,0%']
        Col1_data = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr/td//b') if '-' in i.text or '+' in i.text or i.text == '0,0%']
        Area = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr/td[2]')][1:]
        date = [i.text for i in self.driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div[2]/table[12]/tbody/tr[1]/td/table/tbody/tr/td[3]/small')]

        h = 0
        k =0
        a = 0
        for i in Col1_names:
            if '…' in i:
                for t in Col1[:3]:
                    lst = [[i, Col1[h]], [Area[a],date[a],Col1_data[k], Col1_data[k + 1]]]
                    self.Data.append(lst)
                    k += 2
                    a+=1
                    h+=1

            else:
                lst = [[i],[Area[a],date[a],Col1_data[k], Col1_data[k + 1]]]
                k += 2
                a+=1
                self.Data.append(lst)

        print(self.Data)
        self.to_csv(Header,Headers)

    def to_csv(self,Headers,Header):
            with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(["Price / Quotation","Area","Last",'from prev. price','from 1 year ago'])
                for j in self.Data:
                    print(j)
                    writer.writerow([j[0]]+ j[1])


if __name__ == "__main__":
    Clal_Cheese3().scrape()
