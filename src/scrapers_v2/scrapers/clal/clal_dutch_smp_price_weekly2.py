from scraper_classes.bs4_scraper import Bs4Scraper
import csv


class Clal_SMP(Bs4Scraper):

    def __init__(self,url = ('https://www.clal.it/en/?section=smp_olanda'),CSV_FOLDER_PATH=None):
     super().__init__(url,CSV_FOLDER_PATH)
     self.Data = []
     self.titles = []
     self.d = {}


    def scrape(self):
        el = self.soup.find_all('table',{'width':'98%'})
        date = [i.find('td') for i in el[1] if not None]
        subdata = [i.find('tr') for i in el[1] if not None]
        print(subdata)
        k = 7
        for i in date[7:]:
            try:

                print(i.text.strip())
                value = "".join([x for x in subdata[k].text if x != "\n" and x != "\t"])
                if "-" in value:
                    self.d[i.text.strip()] = [value.split("-")[0], "-" + value.split("-")[1]]
                elif "+" in value:
                    self.d[i.text.strip()] = [value.split("+")[0], "+" + value.split("+")[1]]
                k += 1


            except AttributeError as e:
                k+=1
                continue

        print(self.d)
        #print(el)
        data = [i.find_all('td') for i in el.find_all('td')]
        #for i in data:
            #for j in i:

                #print(j.text)
        #print(data)
        #print(el)
        data  = el.find_all('td', {'class': 'intestazione'})
        for i in data :

            if i.text.strip() not in self.titles:

                self.titles.append(i.text.strip())

        print(self.titles)
        self.to_csv()

    def to_csv(self):
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(self.titles[1:-1])

            for j in self.d.keys():

                writer.writerow([j] + self.d[j])


if __name__ == "__main__":
    Clal_SMP.scrape()
