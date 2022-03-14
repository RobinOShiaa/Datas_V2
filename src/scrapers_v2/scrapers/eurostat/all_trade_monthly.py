

from scraper_classes.chrome_scraper import ChromeScraper
import time
import gzip
import shutil
import os



class Eurostat_Trade(ChromeScraper):


    def __init__(self, url='https://ec.europa.eu/eurostat/web/products-datasets/product?code=ei_eteu28_m', CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.driver.get(url)


    def scrape(self):
        time.sleep(5)
        all_files = set(os.listdir(self.CSV_FOLDER_PATH))

        div = self.driver.find_element_by_class_name('product-section-left')
        self.driver.get(div.find_element_by_tag_name('a').get_attribute('href'))
        time.sleep(3)
        all_files_new = set(os.listdir(self.CSV_FOLDER_PATH))
        new_file_path = self.CSV_FOLDER_PATH + '/' + list(all_files_new - all_files)[0]
        name_of_file = new_file_path.split('/')[-1]
        tsv_name_of_file = '.'.join(name_of_file.split('.')[:-1])
        print(tsv_name_of_file)


        with gzip.open(new_file_path, 'rb') as f_in:
            with open(tsv_name_of_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_out.close()
        f_in.close()
        os.remove(new_file_path)
        self.processFile(tsv_name_of_file)


    def processFile(self,tsv):
        with open('./' + tsv, "r", encoding='utf-8') as f:
            lstInput = []
            for oLine in f:
                try:
                    lstLine = oLine.replace('\n', '').replace(' ','').replace('p','').replace('c','').split('\t')


                except Exception as e:
                    print(e)
                    pass
                lstInput.append(lstLine)
        f.close()
        csv_name_of_file = tsv.split('.')[:-1] + ['.csv']
        with open(self.CSV_FOLDER_PATH + '/' + ''.join(csv_name_of_file), "w+", encoding='utf-8') as f:
            for oLine in lstInput:
                szWriteLine = ",".join(oLine)
                f.write(szWriteLine + '\n')

            f.close()


if __name__ == "__main__":
    Eurostat_Trade().scrape()
