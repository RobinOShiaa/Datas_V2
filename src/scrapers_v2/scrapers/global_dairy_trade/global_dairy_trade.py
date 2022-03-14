from scraper_classes.chrome_scraper import ChromeScraper
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
import csv


class GlobalDairyTrade(ChromeScraper):

    logger = get_logger("GlobalDairyTrade")

    def scrape(self):
        self.logger.info("Starting")
        self.url = "https://www.globaldairytrade.info/en/product-results/"
        self.driver.get(self.url)

        soup = BeautifulSoup(self.driver.page_source, "lxml")

        # List for use in finding event_title
        event_title_tags = soup.find("div", {"class": "moduleEventDetails moduleEventDetailsSummary nextEventDate"})
        # list for use in finding change_in_gdt and average_price. This list should always be len(2)
        gdt_price_index = soup.find_all("div", {"class": "moduleChangePriceIndex"})

        event_title = " ".join([x.text.strip() for x in event_title_tags if "\n" not in x])
        change_in_gdt = (gdt_price_index[0].h4.text,
                         "".join([x.text.strip() for x in gdt_price_index[0].find_all("td") if "\n" not in x]))

        average_price = (gdt_price_index[1].h4.text,
                         "".join([x.text.strip() for x in gdt_price_index[1].div if "\n" not in x]))

        products_tags = soup.find("div", {"class": "productKnobs"})

        # This list contains <div> of Products (Anhydrous Milk Fat, Butter, Butter Milk Powder, etc.)
        products = products_tags.div.find_all("div", {"class", "productFloat"})
        filtered_products = [x.find_all("span") for x in products]

        write_list = []
        write_list.append(["Product", average_price[0], change_in_gdt[0]])
        write_list.append([event_title, average_price[1], change_in_gdt[1]])

        unwanted = ["not offered at this event", "information currently unavailable"]
        # Append final data to write_list
        for product in filtered_products:
            # ['Anhydrous Milk Fat', '$5,530', '-3.3', '%', '-3.3%$5530']
            row = [x.text.strip() for x in product if x.text.strip().lower() not in unwanted]
            if self.is_number(row[1]):
                write_list.append([row[0], row[1], row[2] + row[3]])
            else:
                write_list.append([row[0], "na", "na"])

        # Write write_list to file
        with open(self.CSV_FILE_PATH, "w+", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for row in write_list:
                writer.writerow(row)
        self.logger.info("Finished")

    def is_number(self, x):
        """Method checks whether a string price (e.g. $4,700) contains a valid number."""
        symbols = ["$", "€", "£", "¥"]
        if "n" not in x and "a" not in x:
            if len(x) > 1 and x[0] in symbols:
                x = x[1:]
                if x.isdigit() is True or self.is_decimal(x) is True:
                    return True
                elif "," in x:
                    x = x.split(",")
                    if x[0].isdigit() and x[1].isdigit():
                        return True
        return False

    def is_decimal(self, n):
        """Checks whether a number is a decimal number or not. Method takes a string."""
        n = n.split(".")
        if len(n) == 2:
            if n[0].isdigit() and n[1].isdigit():
                return True
            elif "-" in n[0] and n[0][1:].isdigit():
                return True
        return False


if __name__ == "__main__":
    GlobalDairyTrade().scrape()
