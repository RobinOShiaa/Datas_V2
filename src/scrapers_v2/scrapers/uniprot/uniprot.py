from scraper_classes.chrome_scraper import ChromeScraper
from selenium.webdriver.support.ui import Select
from scrapers.logger import get_logger
from bs4 import BeautifulSoup
from random import choice
import xml.etree.ElementTree as ET
import datetime
import shutil
import string
import gzip
import time
import csv
import os


class UniProt(ChromeScraper):

    logger = get_logger("UniProt")

    def scrape(self, database="uniprot"):
        self.logger.info("Starting")
        if database.lower() in ["uniprot", "uniparc"]:
            tmp_path = self.get_xml_file(database)
            if database is "uniprot":
                self.uniprot_to_csv(tmp_path)
            else:
                self.uniparc_to_csv(tmp_path)
        else:
            return self.logger.error("Invalid user input")
        self.logger.info("Finished")

    def build_xml_chunk(self, entry):
        """Takes a list of Element objects and converts them to XML format as a variable called tags, in string format,
        which it then returns."""
        tags = ""
        for event, elem in entry:
            tag_ = elem.tag[elem.tag.find("}") + 1:]
            if event is "start":
                # If tag has attributes
                if bool(elem.attrib):
                    # Example output: <dbReference type='SUPFAM' id='SSF48445'>
                    tags += "<{} {}>\n".format(tag_, " ".join(["{}='{}'".format(x, elem.attrib[x]) for x in elem.attrib]))
                else:
                    tags += "<{}>\n".format(tag_)
            elif event is "end":
                if elem.text is not None:
                    tags += "{}\n".format(elem.text.strip())
                tags += "</{}>\n".format(tag_)
        return tags

    def uniprot_to_csv(self, tmp_path):
        """Reads an XML file line by line and writes the data to a csv file. Each row's information is within an <entry>
        tag, so I keep looping and appending Element objects to tmp_row list, until I encounter a closing </entry> tag.
        I then call build_xml_chunk(), supplying this tmp_row list to it, which then returns a properly formatted XML
        string, which I pass to a BeautifulSoup object for data extraction. So, at any given time only one <entry> tag
        exists in memory."""
        # Create new csv file
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            self.logger.info("Creating new csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Entry", "Entry name", "Protein name", "Gene names", "Organism", "Keywords", "Length",
                             "Mass", "Checksum", "Sequence"])
            tmp_row = []
            skip = 0
            # Loop through XML file line by line. Event is either 'start', or 'end' (representing start/end of tags)
            for event, elem in ET.iterparse(tmp_path, events=('start', 'end', 'start-ns', 'end-ns')):
                tag = str(elem)
                # If we reach </tag>, call build_xml_chunk() and extract necessary data using BeautifulSoup
                if event is "end" and "entry" in tag:
                    tmp_row.append((event, elem))

                    # Pass an XML string to BeautifulSoup
                    soup = BeautifulSoup(self.build_xml_chunk(tmp_row), "lxml")

                    # The next block of variables is simple data extraction
                    entry = soup.find("accession").text.strip()
                    entry_name = soup.find("name").text.strip()
                    protein_name = soup.find("protein").find("fullname").text.strip()
                    try:
                        gene_names = [tag.text.strip() for tag in soup.find("gene").find_all("name")]
                    except AttributeError:
                        # <gene> tag is missing
                        gene_names = ""
                    organism = " ".join([tag.text.strip() if i == 1 else "({})".format(tag.text.strip())
                                         for i, tag in enumerate(soup.find("organism").find_all("name"), 1)])
                    length = soup.find("sequence").attrs["length"]
                    keywords = [tag.text.strip() for tag in soup.find_all("keyword")]\
                        if len(soup.find_all("keyword")) != 0 else ""
                    mass = soup.find("sequence").attrs["mass"]
                    checksum = soup.find("sequence").attrs["checksum"]
                    sequence = soup.find("sequence").text

                    # Finally, write the extracted data to the csv file
                    writer.writerow([entry, entry_name, protein_name, gene_names, organism, keywords, length, mass,
                                     checksum, sequence])

                    # Reset tmp_row for next <entry>
                    tmp_row = []
                else:
                    # Skip first 3 Element objects because the first <entry> Element starts at index 3
                    if skip > 2:
                        tmp_row.append((event, elem))
                skip += 1
        os.remove(tmp_path)

    def uniparc_to_csv(self, tmp_path):
        """Converts XML file from the UniParc database to a csv file. Same principle as uniprot_to_csv()
        https://www.uniprot.org/uniparc/"""
        # Create new csv file
        with open(self.CSV_FILE_PATH, "w+", newline="", encoding="utf-8") as f:
            self.logger.info("Creating new csv file")
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Entry", "First seen", "Last seen", "UniProtKB", "Length", "Checksum", "Sequence"])
            tmp_row = []
            skip = 0
            # Loop through XML file line by line. Event is either 'start', or 'end' (representing start/end of tags)
            for event, elem in ET.iterparse(tmp_path, events=('start', 'end', 'start-ns', 'end-ns')):
                tag = str(elem)
                # If we reach </tag>, call build_xml_chunk() and extract necessary data using BeautifulSoup
                if event is "end" and "entry" in tag:
                    tmp_row.append((event, elem))

                    # Pass an XML string to BeautifulSoup
                    soup = BeautifulSoup(self.build_xml_chunk(tmp_row), "lxml")

                    # The next block of variables is simple data extraction
                    entry = soup.find("accession").text.strip()

                    # List of sorted dates in ascending order, so [0] == oldest date
                    first_seen = sorted([tag.attrs["created"] for tag in soup.find_all("dbreference") if len(tag.attrs) > 6],
                                        key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))[0]

                    # Newest date is the last element of the list
                    last_seen = sorted([tag.attrs["last"] for tag in soup.find_all("dbreference") if len(tag.attrs) > 6],
                                       key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))[-1]
                    uni_prot_kb = [tag.attrs["id"] for tag in soup.find_all("dbreference") if len(tag.attrs) > 6]
                    length = soup.find("sequence").attrs["length"]
                    checksum = soup.find("sequence").attrs["checksum"]
                    sequence = soup.find("sequence").text

                    # Finally, write the extracted data to the csv file
                    writer.writerow([entry, first_seen, last_seen, uni_prot_kb, length, checksum, sequence])

                    # Reset tmp_row for next <entry>
                    tmp_row = []
                else:
                    # Skip first 3 Element objects because the first <entry> Element starts at index 3
                    if skip > 2:
                        tmp_row.append((event, elem))
                skip += 1
        os.remove(tmp_path)

    def get_xml_file(self, database):
        """Downloads an XML file from UniProtKB or UniParc, and returns the path to the file."""
        # Get a set of current files in csv_files, to later find out which is the new (downloaded) file
        files = set(os.listdir(self.CSV_FOLDER_PATH))

        self.driver.get("https://www.uniprot.org/{}/".format(database))

        # Navigating the website. Click 'Download', select drop down menu, select XML, and click 'Go' (download button)
        #self.driver.find_element_by_id("download-button").click()
        #select = Select(self.driver.find_element_by_id("format"))
        #select.select_by_value("xml")
        #self.driver.find_element_by_id("menu-go").click()
        #logger.info("Downloading GZ file")

        # For testing
        self.driver.find_element_by_id("selectAll-resultSet").click()
        self.driver.find_element_by_id("download-button").click()
        self.driver.find_element_by_xpath("//*[@id='selected']").click()
        select = Select(self.driver.find_element_by_id("format"))
        select.select_by_value("xml")
        self.driver.find_element_by_id("menu-go").click()
        self.logger.info("Downloading XML file")

        self.wait_for_download_to_complete()

        # Lambda function to generate random name for the new XML file
        random_name =\
            lambda x: "".join(choice(string.ascii_lowercase + string.digits) for _ in range(14))

        new_xml_path = self.CSV_FOLDER_PATH + "/" + random_name("") + ".xml"

        # Unzip downloaded file (.gz), so that we can extract the XML file from it
        new_gz_path = self.CSV_FOLDER_PATH + "/" + list(set(os.listdir(self.CSV_FOLDER_PATH)) - files)[0]
        with gzip.open(new_gz_path, "rb") as f_in:
            with open(new_xml_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove downloaded file (not needed anymore)
        os.remove(new_gz_path)
        return new_xml_path

    def wait_for_download_to_complete(self):
        """Check every 5 seconds whether the file has finished downloading. This is a necessary 'wait' method because
        selenium doesn't have one, and we need to wait for the download to finish before continuing code execution."""
        while True:
            if len([file for file in os.listdir(self.CSV_FOLDER_PATH) if file[-3:] == ".gz"]) != 0:
                return
            time.sleep(5)


#UniProt().scrape("uniprot")
#UniProt().scrape("uniparc")