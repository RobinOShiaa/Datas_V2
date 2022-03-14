from scraper_classes.bs4_scraper import Bs4Scraper
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
import requests


class Alic(Bs4Scraper):

    logger = get_logger("Alic")

    def scrape(self, categories=None):
        if categories is None:
            excel_dict = self.html_table_to_dict()
        else:
            excel_dict = self.html_table_to_dict(categories)

        # Loop through keys
        for category in excel_dict:
            # Loop through values of keys
            for row in excel_dict[category]:
                self.download_xlsx(row)
        self.logger.info("Finished")

    def html_table_to_dict(self, user_categories=None):
        """This method scrapes the html table, creating a dictionary of data in the following format and returns it:
        excel_dict = {
                        'Beef and Cattle':  [
                                                ['Supply and Demand of Beef', Excel_1, Excel_2, Excel_3],
                                                ['Cattle Slaughtering(1)', Excel_1, Excel_2, Excel_3],
                                                ['Cattle Slaughtering(2)', Excel_1, Excel_2, Excel_3]
                                            ]
        }

        Users may also specify which categories they wish to scrape. Valid categories are the titles of tables. At the
        time of writing this code, the valid categories were:

        ["Supply and Demand for Livestock Products", "Meat relation", "Beef and Cattle", "Pork and Hog", "Broiler",
        "Milk and Dairy Products", "Egg"]"""
        self.url = "http://lin.alic.go.jp/alic/statis/dome/data2/e_nstatis.htm"
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "lxml")

        # This is the <tr> tag with all of the table entries (names, categories, excel links)
        soup = soup.find("tr", {"style": "mso-yfti-irow:3;height:16.5pt"})

        # If user specified categories then only keep those from soup.find_all("div")[1:]
        if user_categories is not None:
            categories = [x for x in soup.find_all("div")[1:]
                          if x.a.text.lower() in [x.lower() for x in user_categories]]
        else:
            categories = soup.find_all("div")[1:]

        excel_dict = {}
        # Loop through table categories ("Supply and Demand for Livestock Products", "Meat relation", etc.)
        for category in categories:
            category_name = category.a.text

            # Loop through each row of current category
            for row in category.find_all("tr")[2:]:
                row_ = row.find_all("td")
                row_without_excel = row.p.text.strip()

                # material_names is a list of <p> tags. It's len 1 most of the time. However, in some cases its len is
                # higher than 1, in which case you need to "".join() them to have the proper row name (material name).
                material_names = row_[len(row_)-4].find_all("p")

                row_name = [x.text.strip() if len(material_names) == 1 else
                            "".join([x.text.strip() for x in material_names]) for x in material_names][0]

                # If this row is not empty (i.e. contains Excel files)
                if row_name != row_without_excel:
                    urls = row_[len(row_)-3:]

                    # If current category is not in dictionary yet
                    if category_name not in excel_dict:
                        excel_dict[category_name] = [[row_name] +
                                                     [x.a["href"] if x.a is not None else "Null" for x in urls]]
                    # If current category is already in dictionary, just append to the list excel_dict[category_name] is pointing to
                    else:
                        excel_dict[category_name].append([row_name] +
                                                         [x.a["href"] if x.a is not None else "Null" for x in urls])
        return excel_dict

    def download_xlsx(self, urls):
        """Method downloads Excel files from list of URLs supplied. It accepts a list of the following format:
        urls = ['Supply and Demand of Beef', Link_1, Link_2, Link_3]"""

        # file_ending will be used as part of the file name
        file_ending = ["recent 15 months data", "previous data", "fiscal year data"]
        i = 0
        for url in urls[1:]:
            if url is not "Null":
                result = requests.get(url)
                with open(self.CSV_FOLDER_PATH + "/{}_{}.xlsx".format(urls[0].lower(), file_ending[i]), "wb") as f:
                    f.write(result.content)
                print("{}_{}.xlsx".format(urls[0].lower(), file_ending[i]))
            i += 1


if __name__ == "__main__":
    Alic().scrape()
