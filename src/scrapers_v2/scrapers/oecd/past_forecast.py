import time
from scraper_classes.chrome_scraper import ChromeScraper

class Past_Forecast(ChromeScraper):

    def __init__(self, url, CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        self.Variables = {}
        self.todo = []
        self.features = {}

        self.driver.get(url)
        self.driver.maximize_window()


    def choose_variables(self):
        print('Please enter name out of following topics')
        while True:
            line = input()
            if line in self.Variables:
                self.Variables[line].click()

            else:
                break



    def scrape(self):
        time.sleep(5) # implicitly_wait doesn't wait for alert box
        try:
            self.driver.switch_to_alert().accept()
        except:
            pass

        keys = self.get_dropdown_list('id', 'PDim_VARIABLE')
        values = self.get_dropdown_list('id', 'PDim_VARIABLE', 'text')
        self.features = dict(zip([x.split("~")[1].strip() for x in keys], [k.split("~")[1].strip() + " " + v.strip() for k, v in zip(keys, values)]))
        print(self.features)

        self.data_to_take()



    def data_to_take(self):
        self.driver.find_element_by_xpath('//*[@id="tabletofreeze"]/table/thead/tr[2]/th[1]/b/a').click()
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
        for i in dictionary.keys():
            print(i)
        self.choose_variables()





        self.driver.find_element_by_xpath('//*[@id="lbtnViewData"]').click()
        time.sleep(6)
        self.to_csv()

    def to_csv(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="menubar-export"]/a').click()
        self.driver.find_element_by_xpath('//*[@id="ui-menu-2-1"]').click()
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


t = Past_Forecast('https://stats.oecd.org/viewhtml.aspx?QueryId=48184&vh=0000&vf=0&l&il=&lang=en#')
t.scrape()

