# Class Structure
## Base `Scraper` class explained
The base class takes one required argument, a `URL` of the website to be scraped. There is also an optional 2nd argument, which is a path to where a folder called `csv_files` will be created (if it doesn't already exist). This is where `csv` files will be written. If no path is supplied, the `__init__()` method will dynamically generate a suitable one, and it works on both Windows and Linux. A `csv` name and path are also generated from within the `__init__()` method. The name is a string of current date and time, and the path is the `csv_files` path + `csv` name. The `csv_files` will be created from wherever the actual `.py` script is executed. For example if it's executed from `C:\Project\script.py`, then a folder is created at `C:\Project\csv_files`.

## Child classes
The base class, `Scraper`, has four child classes which inherit from it. These are: `Bs4Scraper`, `UrllibScraper`, `ChromeScraper`, and `FirefoxScraper`. The actual scrapers then inherit from one of these four classes.

## `ChromeScraper` and ` FirefoxScraper`
The `__init__()` method of these two classes has a way to point the `chromedriver`/`geckodriver` to its path in Windows's `PATH` environment variable. If `chromedriver`/`geckodriver` is not found in `PATH`, then the user gets notified and object initialisation is aborted. The method also changes the download directory to the dynamic `csv_files` folder, so the programmer doesn't have to worry about finding the `Downloads` directory.
