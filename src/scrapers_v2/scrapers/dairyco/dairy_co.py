from scraper_classes.chrome_scraper import ChromeScraper

from xlrd import open_workbook
import time
import csv
class dairyco(ChromeScraper):



    def __init__(self, url = ('https:/dairy.ahdb.org.uk/resources-library/market-information/supply-production/daily-milk-deliveries/#.XRIVkuhKi71'), CSV_FOLDER_PATH=None):
     super().__init__(url, CSV_FOLDER_PATH)
     self.driver.get(url)
     self.download()

    def download(self):
        link = self.driver.find_element_by_xpath('/*[@id="wrapper"]/div[6]/div[2]/div/div/a').get_attribute('href')
        self.driver.get(link)





time.sleep(5)
wb = open_workbook('./csv_files/new_uk_daily_milk_deliveries_with_forecast.xls')

for i in range(wb.nsheets):
    try:
        sheet = wb.sheet_by_index(i)
        print(sheet.name)
        with open("./csv_files/%s.csv" %(sheet.name.replace(" ","")), "w+") as file:
            writer = csv.writer(file, delimiter = ",")
            print(sheet, sheet.name, sheet.ncols, sheet.nrows)
            header = [cell.value for cell in sheet.row(0)]
            writer.writerow(header)
            for row_idx in range(sheet.nrows):
                row = [cell.value for cell in sheet.row(row_idx)]
                writer.writerow(row)
    except IndexError as e:
        break
if __name__ == "__main__":
    dairyco().scrape()
