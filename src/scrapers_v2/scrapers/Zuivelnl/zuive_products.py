
import PyPDF2 as p2

import csv

from datetime import datetime

from scraper_classes.chrome_scraper import ChromeScraper

class ZuiveProd(ChromeScraper):

    def __init__(self, url = 'https://www.zuivelnl.org/wp-content/uploads/2019/06/Productie-2019.pdf', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)

        self.driver.get(url)
        self.driver.maximize_window()
        self.table = {}


    def scrape(self):

        i = -1
        while i < 37:
            try:
                i += 1
                self.open_pdf(i)
                print(self.table.keys())
            except:
                break


    def open_pdf(self,i):

        PDFfile = open(self.CSV_FOLDER_PATH + "/Productie-2019.pdf",'rb+')
        PDFtext = open(self.CSV_FOLDER_PATH + "/Productie-2019.txt", 'w+')
        pdfread = p2.PdfFileReader(PDFfile)
        #print(pdfread.getNumPages())

        x = pdfread.getPage(i)
        PDFtext.write(x.extractText())
      #  print(x.extractText())

        PDFfile.close()
        PDFtext.close()

        with open(self.CSV_FOLDER_PATH + "/Productie-2019.txt", 'r') as f:
            lines = f.readlines()
           # print(lines)
            new_list = []
            for line in lines:
                if (line.strip().split('\n')[0]) != '' and line.strip().split('\n')[0] != 'v':
                     new_list += (line.strip().split('\n'))
                     print(line.strip().split('\n'))



            start = new_list.index('jan') - 1
            end = new_list.index('index') + 1
            Headers = (new_list[start:end])
            #print(Headers)
            #print(new_list)
            i = end
            row = []
            rows = [Headers]

            while i < len(new_list):

                if len(row) == len(Headers):
                    rows.append(row)
                   # print(row)
                    row = []

                row.append(new_list[i])
                i+=1

            #print(rows)
            for row in rows:
                #print(row)
                #self.table[i[0]] = i
                #k = self.table[i[0]]
                #if Headers[1]  != i[1]:
                #    k = i
                if "index" not in row:
                    self.table[title].append(row)
                else:
                    title = row[0]
                    self.table[title] = []
            print(self.table)
            print(len(self.table))



            print(self.table)

            #print(rows)
            self.to_csv(Headers)

            f.close()
            #os.remove(self.CSV_FOLDER_PATH + '/Productie-2019.pdf')
            #os.remove(self.CSV_FOLDER_PATH + '/Productie-2019.txt')
    def to_csv(self,Headers):
        for i in self.table.keys():
            if i == 'Nederland*':
                with open(self.CSV_FOLDER_PATH + '/Products/Nederland2.csv', "w+", newline="") as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    writer.writerow(Headers)
                    print(self.table[i])
                    for value in self.table[i]:
                        writer.writerow(value)
            else:
                with open(self.CSV_FOLDER_PATH + '/Products/{}_{}.csv'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),i), "w+", newline="") as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    writer.writerow(Headers)
                    print(self.table[i])
                    for value in self.table[i]:
                        writer.writerow(value)


            #for line in lines:
             #   print(line.strip())





if __name__ == "__main__":
    ZuiveProd().scrape()






