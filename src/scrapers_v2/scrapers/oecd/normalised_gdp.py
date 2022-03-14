import time

from scraper_classes.chrome_scraper import ChromeScraper

class Normalised_gdp_data(ChromeScraper):

    def __init__(self, url, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.Variables = {}
        self.todo = []
        self.features = {}

        self.driver.get(url)
        self.driver.maximize_window()


    def scrape(self):



        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[14]').click()  # Monthly Economic Indicators
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[14]/ul/li[1]').click()# Composite Leading Indicators
        self.driver.find_element_by_xpath('//*[@id="browsethemes"]/ul/li[14]/ul/li[1]/ul/li').click()# Composite Leading Indicators (MEI)


        time.sleep(3) # implicitly_wait doesn't wait for alert box
        try:
            self.driver.switch_to_alert().accept()
        except:
            pass

        time.sleep(6)

        self.to_csv()

    def to_csv(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="ui-menu-0-1"]').click()
        time.sleep(3)
        self.driver.switch_to.frame('DialogFrame')
        self.driver.execute_script("$('#_ctl12_btnExportCSV').click()")







    def get_dropdown_list(self, attr_name, attr_value, result_type='value'):
        """Get all option values in a dropdown list"""
        dropdown_box = None

        if attr_name == 'id':
            dropdown_box = self.driver.find_element_by_id(attr_value)
        elif attr_name == 'name':
            dropdown_box = self.driver.find_element_by_name(attr_value)

        # get all objects in the dropdown list
        # TODO(Wenchong): add more find_elements_by options

        options = [x for x in dropdown_box.find_elements_by_tag_name('option')]
        results = []

        if result_type == 'value':
            # get the values of all dropdown list objects
            for option in options:
                results.append(str(option.get_attribute('value')))
        elif result_type == 'text':
            # get the texts of all dropdown list objects
            for option in options:
                results.append(str(option.text))

        return results


t = Normalised_gdp_data('https://stats.oecd.org/')
t.scrape()

