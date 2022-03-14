# Documentation
## Purpose
This class downloads an `XML` file from [UniProtKB](https://www.uniprot.org/uniprot/) or [UniParc](https://www.uniprot.org/uniparc/), and converts it to a `csv` file.

## Notes
* The databases currently contain between 159 million - 273 million entries, so the `XML` file will take a long time to download, especially because the website seems to heavily throttle the download speed.

## Implementation
* `get_xml_file()` downloads an `XML` file and returns its path for further use.
* `uniprot_to_csv()` and `uniparc_to_csv()` have identical logic, just different data.
* `uniprot_to_csv()` and `uniparc_to_csv()` read an `XML` file line by line, so the memory usage is low. The main problem with this is that you don't have a built in way of knowing which entry/row you are currently looping through. However, one row of data in [UniProtKB](https://www.uniprot.org/uniprot/)/[UniParc](https://www.uniprot.org/uniparc/) is contained within an `<entry></entry>` tag in the `XML` file, so I keep appending tags (which are `Element` objects) to a temporary list. When I reach a closing `</entry>` tag  I pass this list to `build_xml_chunk()`, which it then converts the list to `XML` format, returning it as a string. This string can then be passed to a `BeautifulSoup` object, which I use for the data extraction itself. At this point it's very simple data extraction, and lastly you write the extracted data to the `csv` file.

## UniProtKB
> The UniProt Knowledgebase (UniProtKB) is the central hub for the collection of functional information on proteins, with accurate, consistent and rich annotation. In addition to capturing the core data mandatory for each UniProtKB entry (mainly, the amino acid sequence, protein name or description, taxonomic data and citation information), as much annotation information as possible is added.

## UniParc
> UniParc is a comprehensive and non-redundant database that contains most of the publicly available protein sequences in the world. Proteins may exist in different source databases and in multiple copies in the same database. UniParc avoids such redundancy by storing each unique sequence only once and giving it a stable and unique identifier (UPI).
