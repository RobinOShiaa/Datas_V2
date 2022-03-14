
from scraper_classes.bs4_scraper import Bs4Scraper
import csv


class Clal_Dairy(Bs4Scraper):

    def __init__(self,url = ('https://www.clal.it/en/?section=burro_francia%22,%22http://www.clal.it/en/index.php?section=poudre'),CSV_FOLDER_PATH=None):
     super().__init__(url,CSV_FOLDER_PATH)
     self.Data = []


    def scrape(self):
        el = self.soup.find("table",{'class':'tabelle_milk'})
        print(el)
        a = [i.find("a").text.strip() for i in el.find_all("td") if i.find("a") is not None]
        countries = [a[:-2]]

        #print(a)
        values = [i.find("i").text.strip() for i in el.find_all("td") if i.find('i') is not None]
        print(values)
        titles = [i.text.strip() for i in el.find_all("td") if i is not None][:6]
        #titles.replace('Δ'," ")

        indx = 0
        d = {}
        k = 0
        last_col = [i.text.strip() for i in el.find_all("td",{'class':'value0'}) if '\n' not in i ]
        print(last_col)
        last_col2 = [i.text.strip() for i in el.find_all("td",{'class':'value1'})  if '\n' not in i]
        print(last_col2)


        last = []
        counter = 0
        while counter < len(last_col2):
            last.append(last_col[counter])
            last.append(last_col2[counter])
            counter+=1


        print(last)
        for i in countries[0]:

            print("I is ",i)
            country_d = values[indx:len(titles)-2 +indx]
            indx += len(titles) -2
            country_d.append(last[k])
            k+=1
            print(country_d)
            d[i] = country_d
            print("d is ",d)

            self.Data.append(d)
        print(self.Data)


        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([t for t in titles])
            for j in self.Data[0].keys():
                writer.writerow([j] + [i for i in self.Data[0][j]])


if __name__ == "__main__":
    Clal_Dairys().scrape()
