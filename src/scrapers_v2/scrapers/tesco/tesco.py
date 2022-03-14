from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
from selenium import common
import csv


class Tesco(ChromeScraper):

    logger = get_logger("Tesco")

    def scrape(self):
        self.logger.info("Starting")
        # Create dictionary of navigation menus
        menu_dict = self.get_menu_dict()
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            self.logger.info("Creating new csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Category", "Subcategory", "Product", "Price", "Price/Unit", "Unit"])
            # Loop through top level menus
            for menu in menu_dict:
                # Loop through sub menus
                for sub_menu in menu_dict[menu][1].items():
                    category = sub_menu[0]
                    sub_menu_url = sub_menu[1]

                    # Go to new URL and create a new BeautifulSoup object with the new URL's data
                    self.driver.get(sub_menu_url)
                    soup = BeautifulSoup(self.driver.page_source, "lxml")

                    # Call scrape_products() to get data for current page
                    current_products = self.scrape_products(soup, menu, category)
                    if current_products == -1:
                        # self.scrape_products() returns -1 when a missing page is encountered
                        break

                    # Loop through rows of dictionary and write them line by line to the csv file
                    for row in current_products:
                        writer.writerow([menu, category, row] + current_products[row])

                    # This block of code is for clicking 'next' (page), scraping the products, and writing to file.
                    # It's the same kind of thing as above, but it has to be within a new loop to go through the pages.
                    while True:
                        try:
                            self.driver.find_element_by_class_name("next").click()

                            # Get current URL after clicking on 'next'
                            self.driver.get(self.driver.current_url)
                            soup = BeautifulSoup(self.driver.page_source, "lxml")

                            current_products = self.scrape_products(soup, menu, category)
                            if current_products == -1:
                                break

                            for row in current_products:
                                writer.writerow([menu, category, row] + current_products[row])
                        # These two exceptions occur when you reach the last page (i.e. 'next' doesn't exist)
                        except (common.exceptions.ElementNotInteractableException,
                                common.exceptions.ElementNotVisibleException):
                            break
        self.driver.close()
        self.logger.info("Finished")

    def scrape_products(self, soup, menu, category):
        """Method scrapes products from current page and returns them in a dictionary of the following format:
        name_price_dict = {
                                "Jack Daniel's Tennessee Whiskey 70Cl": ["€34.00", "€48.58", "l"],
                                "Hennessy VS Cognac": ["€36.00", "€51.43", "l"]
        }"""
        self.logger.info("Scraping " + menu + ", " + category + " at: " + self.driver.current_url)
        # Scrape products
        try:
            products_tags = soup.find("div", {"class", "productLists"}).find_all("li")
        except AttributeError as e:
            # Current sub_menu is probably non-existent (exists in footer, but not in drop down menu)
            self.logger.error("Error: ", str(e))
            self.logger.info("Possible cause of Exception: sub menu exists in Footer menus, but not in drop down menus.")
            return -1

        # Function expects ['€0.22', '(€1.25/each)'] and returns ['€0.22', '€1.25', 'each']
        lmb = lambda x: [x[0], x[1].split("/")[0][1:], x[1].split("/")[1][:-1]]

        product_names = [tag.a.text.strip() for tag in products_tags if "\n" not in tag.a.text.strip()]
        product_prices = [lmb(tag.find("p", {"class": "price"}).text.strip().split(" ")) for tag in products_tags
                          if tag.find("p", {"class": "price"}) is not None]

        # Convert product_names and product_prices lists into dict of format: d = {'Carrot': ['€0.25', '€1.49', 'kg']
        name_price_dict = dict(zip(product_names, product_prices))
        return name_price_dict

    def get_menu_dict(self):
        """Returns a dictionary of the navigation menus in the following format:
        menu_dict = {
                        "Fresh Food": [URL, {
                                            "sub_menu_1": URL,
                                            "sub_menu_2": URL,
                                            "sub_menu_3": URL
                        }],
                        "Bakery":           [URL, {}],
                        "Food Cupboard":    [URL, {}]
        }"""
        self.logger.info("Creating menu dictionary")
        self.url = "https://www.tesco.ie/groceries/"

        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        # List of navigation menus (Fresh Food, Bakery, Food Cupboard, etc.)
        second_level_menu = soup.find("ul", {"class": "navigation Groceries"}).find_all("li")

        # {second_level_menu: URL} dictionary
        menu_dict = {tag.a.text: [tag.a.attrs["href"]] for tag in second_level_menu}

        # Loop through menus
        for menu in menu_dict:
            # Go to new URL (menu), and re-create BeautifulSoup with the new URL's content
            self.driver.get(menu_dict[menu][0])
            soup = BeautifulSoup(self.driver.page_source, "lxml")

            # These are the menus at the bottom of the web page. It's easier to get than using the drop down menus.
            footer_menus = soup.find_all("div", {"class", "mboxDefault"})[-1].find("div", {"class", "footer"}).find_all("a")

            # Append sub menus to list {"Fresh Food": [URL, {new_dict_here}]}
            menu_dict[menu].append({tag.text: tag.attrs["href"] for tag in footer_menus
                                    if tag.text.lower() != "charity of the year contribution"})

        # Click 'Hide images' before returning
        for menu in menu_dict:
            first_sub_menu_url = next(iter(menu_dict[menu][1].values()))
            self.driver.get(first_sub_menu_url)
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            try:
                self.driver.get(soup.find("a", {"class": "prodImageToggle hideImages"}).attrs["href"])
            except:
                # 'Hide images' not found
                self.logger.error("Hide images button not found")
                break
            break
        return menu_dict


if __name__ == "__main__":
    Tesco().scrape()
