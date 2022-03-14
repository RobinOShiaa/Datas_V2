from scraper_classes.chrome_scraper import ChromeScraper
from selenium.webdriver.support.ui import Select
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
import time
import csv


class Pig333(ChromeScraper):

    logger = get_logger("Pig333")

    def scrape(self):
        self.logger.info("Starting")
        self.url = "https://www.pig333.com/markets_and_prices/"
        self.driver.get(self.url)

        # Click login. [0] == Signup, [1] == Login
        self.driver.find_element_by_id("div_barra_usuari").find_elements_by_tag_name("button")[1].click()

        # Enter email & password and login
        self.driver.find_element_by_id("input_email").send_keys("daniel.perecz2@mail.dcu.ie")
        self.driver.find_element_by_id("input_pass").send_keys("myprecious")
        self.driver.find_element_by_id("boto_login_div_registre").click()
        time.sleep(self.SECONDS)

        # Click on Price & select 100kg
        self.driver.find_element_by_class_name("form-inline").find_element_by_class_name("form-control").\
            find_elements_by_tag_name("label")[-1].click()
        Select(self.driver.find_element_by_id("select_unitats")).select_by_value("100kg")

        # Create new csv file
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            self.logger.info("Creating new csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Continent", "Country", "Date", "Price EUR/100kg", "Difference", "Difference Percentage"])

            # Wait for page source to update
            time.sleep(self.SECONDS)

            soup = BeautifulSoup(self.driver.page_source, "lxml")
            continents = soup.find("div", {"id": "div_wrap_taules_merats"}).find_all("div", {"class": "contingut continent_preus"})
            for continent in continents:
                tmp_row = {"continent": "na", "country": "na", "date": "na", "price": "na", "difference": "na", "difference percentage": "na"}
                for country in continent.find_all("div")[2:]:
                    tmp_row["continent"] = continent.a.text.strip()
                    tmp_row["country"] = country.a.text
                    tmp_row["date"] = country.find("span", {"class": "bloc bloc2"}).span.text
                    try:
                        tmp_row["price"] = country.find("span", {"class": "bloc bloc2"}).find("span", {"class": "preu_mercat"}).text.split(" ")[0]
                        tmp_row["difference"] = country.find("span", {"class": "bloc bloc_diferencia"}).find_all("span")[0].text
                        tmp_row["difference percentage"] = country.find("span", {"class": "bloc bloc_diferencia"}).find_all("span")[1].text
                    except IndexError:
                        # No info available for current country
                        pass
                    writer.writerow([value for value in tmp_row.values()])
        self.logger.info("Finished")


if __name__ == "__main__":
    Pig333().scrape()
