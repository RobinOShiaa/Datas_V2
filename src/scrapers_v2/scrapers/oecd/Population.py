import time

from scraper_classes.chrome_scraper import ChromeScraper


class Population(ChromeScraper):

    def __init__(self, url, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.Variables = {}
        self.todo = []
        self.features = {}

        self.driver.get(url)
        self.driver.maximize_window()

    def scrape(self):
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[3]/span').click() # 'Demography and Population'
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/span').click() # 'Population Statistics'
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[3]/ul/li[2]/ul/li[1]/a[2]').click()
        time.sleep(5) # implicitly_wait doesn't wait for alert box
        try:
            self.driver.switch_to_alert().accept()
        except:
            pass

        self.to_csv()

    def to_csv(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="ui-menu-0-1"]').click()
        time.sleep(3)
        self.driver.switch_to.frame('DialogFrame')
        self.driver.execute_script("$('#_ctl12_btnExportCSV').click()")




t = Population('https://stats.oecd.org')
t.scrape()

