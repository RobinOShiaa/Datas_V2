from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
import json
import urllib.request
from bs4 import BeautifulSoup


logger = get_logger("Asda")


class Asda(ChromeScraper):

    def __init__(self, url="https://groceries.asda.com/cmscontent/json/pages/site-map", CSV_FOLDER_PATH=None):
        super().__init__(url, CSV_FOLDER_PATH)
        logger.info("Starting")

    def scrape(self):
        menu_dict = self.get_menu_dict()
        # Loop through menu_dict
        # if "View All" in 3rd lvl menu: click on it, else: loop through the menus individually
        # if "cmlisting" in URL, skip (these take us to a completely different page)

        print(menu_dict)

        # Loop through top level menus
        for menu in menu_dict:
            for sub_menu in menu_dict[menu].items():
                sub_menu_name = sub_menu[0]
                sub_menu_url = sub_menu[1]

                #self.driver.get(sub_menu_url)
                url = "https://groceries.asda.com/cmscontent/json/pages/browse/menu?Endeca_user_segments=anonymous%7Cstore_4565%7Cwapp%7Cvp_S%7CZero_Order_Customers%7CDelivery_Pass_Older_Than_12_Months%7CNon_Baby_Customers%7Cdp-false%7C1007%7C1019%7C1020%7C1023%7C1024%7C1027%7C1038%7C1041%7C1042%7C1043%7C1047%7C1053%7C1055%7C1057%7C1059%7C1067%7C1070%7C1082%7C1087%7C1097%7C1098%7C1099%7C1100%7C1102%7C1105%7C1107%7C1109%7C1110%7C1111%7C1112%7C1116%7C1117%7C1119%7C1123%7C1124%7C1126%7C1128%7C1130%7C1140%7C1141%7C1144%7C1147%7C1150%7C1152%7C1157%7C1159%7C1160%7C1165%7C1166%7C1167%7C1169%7C1170%7C1172%7C1173%7C1174%7C1176%7C1177%7C1178%7C1179%7C1180%7C1182%7C1183%7C1184%7C1186%7C1187%7C1189%7C1190%7C1191%7C1194%7C1196%7C1197%7C1198%7C1201%7C1202%7C1204%7C1206%7C1207%7C1208%7C1209%7C1210%7C1213%7C1214%7C1216%7C1217%7C1219%7C1220%7C1221%7C1222%7C1224%7C1225%7C1227%7C1231&storeId=4565&shipDate=1562029200000&N=103214&requestorigin=gi&_=1562069152997"
                response = urllib.request.urlopen(url)
                json_r = json.load(response)

                #self.driver.get(sub_menu_url)

                self.driver.get('https://groceries.asda.com/dept/fresh-food-bakery/fruit/_/103214')
                print(self.driver.find_element_by_id("mainContainer").get_attribute("role"))


                #with open(self.CSV_FOLDER_PATH + '/data.json', 'w', encoding='utf-8') as f:
                #    json.dump(json_r, f, ensure_ascii=False, indent=4)

                #menu_html = json_r["contents"][0]["mainContent"][0]["contents"][0]["content"]
                #soup = BeautifulSoup(menu_html, "html.parser")

                break
            break

    def get_menu_dict(self):
        """Returns a dictionary of the navigation menus in the following format:
        menu_dict = {
                        "Fresh Food": {"Fruit": URL, "Vegetables & Potatoes": URL},
                        "Chilled Food": {"Mill, Butter & Eggs": URL, "Cheese": URL}
        }
        The keys are the main nav menus, and the values are dictionaries of the sub menus.

        Notes on implementation:
        https://groceries.asda.com/site-map has a clean list of all of the menus, however, the HTML doesn't exist when
        trying to scrape using either Selenium or BeautifulSoup, but I was able to grab all of this info through
        their API, specifically through XMLHttpRequest (XHR). Calling the URL below results in JSON data, which includes
        the whole nav menu. The variable menu_html is simply pointing to the JSON data containing the nav menus."""

        response = urllib.request.urlopen(self.url)

        # Load JSON data in dictionary format
        json_r = json.load(response)

        # Get the site map from within the JSON dictionary
        menu_html = json_r["contents"][0]["mainContent"][0]["contents"][0]["content"]
        soup = BeautifulSoup(menu_html, "html.parser")

        # Find all of the names of the top level menus (Fresh Food, Chilled Food, Food Cupboard, etc.)
        h3_tags = soup.find_all("h3")

        # A list of <ul> tags which themselves contain <a> tags. One <ul> contains all of the <a> tags (names & links)
        # of the sub menus. We only need [5:] because we're not interested in the first few nav menus.
        sub_page_tags = soup.find_all("ul")[5:]

        # Dictionary of top level menu names pointing to dictionaries (empty at this point). {"Fresh Food": {}}
        menu_dict = {tag.text: {} for tag in h3_tags if tag.a is not None}

        # List of dictionaries of the sub menus.
        # [{"Fruit": URL, "Vegetables & Potatoes": URL}, {"Mill, Butter & Eggs": URL, "Cheese": URL}]
        sub_pages_name_to_href = [{tag.text.strip(): tag.attrs["href"] for tag in tags.find_all("a")} for tags
                                  in sub_page_tags]

        # Now append the sub menu dictionaries to their corresponding top level menus
        i = 0
        for menu in menu_dict:
            menu_dict[menu] = sub_pages_name_to_href[i]
            i += 1
        return menu_dict


Asda().scrape()

"""
References:
https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
example api call: https://groceries.asda.com/api/items/search?keyword=yogurt%27
"""
