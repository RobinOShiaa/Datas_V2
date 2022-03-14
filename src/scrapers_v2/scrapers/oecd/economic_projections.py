import time
import glob
import os
from scraper_classes.chrome_scraper import ChromeScraper

class Economic_Projections(ChromeScraper):

    def __init__(self,url = 'https://stats.oecd.org/', CSV_FOLDER_PATH = None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.Variables = {}
        self.index = -1
        self.driver.get(url)
        self.driver.maximize_window()
        self.url = ''


    def scrape(self):

        self.economic_projections()

    def economic_projections(self):

        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[5]').click()  # 'Economic projections'
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[5]/ul/li').click()               # 'OECD economic outlook'
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]').click() # 'OECD economic outlook latest edition'
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]/ul/li[1]').click()  # most recent projections
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[5]/ul/li/ul/li[2]/ul/li/ul/li[1]/a[2]').click()
        time.sleep(2)
        self.url = self.driver.current_url
        time.sleep(5) # implicitly_wait doesn't wait for alert box
        try:
            self.driver.switch_to_alert().accept()
        except:
            pass
        self.data_to_take()

    def data_to_take(self):
        self.index +=1
        self.driver.find_element_by_xpath('//*[@id="fixedheader"]/table/thead/tr[1]/th[1]/b/a').click()
        self.driver.switch_to.frame('DialogFrame')
        self.driver.find_element_by_id('lbtnClear_all').click()
        elevator_shake = [e for e in self.driver.find_element_by_id("M_WebTreeDimMembers_1").find_elements_by_tag_name("div") if e.get_attribute('igtag') != None]
        checkboxes = []
        titles = []
        print('please wait')
        for hand in elevator_shake:
            titles.append(hand.get_attribute("title"))
            checkboxes.append(hand.find_element_by_tag_name("input"))
        dictionary = dict(zip(titles,checkboxes))
        self.Variables = dictionary
        if self.index <= len(self.Variables.keys()):
            self.Variables[list(self.Variables.keys())[self.index]].click()
            file_name = list(self.Variables.keys())[self.index]
            self.driver.find_element_by_xpath('//*[@id="lbtnViewData"]').click()
            time.sleep(5)
            self.to_csv()
            time.sleep(4)
            list_of_files = glob.glob(self.CSV_FOLDER_PATH + '/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            file_name = self.CSV_FOLDER_PATH + '/' + file_name.split()[0]
            os.rename(latest_file, file_name)

            self.driver.get(self.url)
            time.sleep(3)
            self.economic_projections()


        print('done')


    def to_csv(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="ui-menu-2-1"]').click()
        time.sleep(3)
        self.driver.switch_to.frame('DialogFrame')
        self.driver.execute_script("$('#_ctl12_btnExportCSV').click()")


if __name__ == "__main__":
    Economic_Projections().scrape()
