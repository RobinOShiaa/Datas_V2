# Documentation
## Purpose
Downloads, fixes, and concatenates data from [stats.govt.nz](http://archive.stats.govt.nz/infoshare/TradeVariables.aspx) to `csv` file. The three statistics that this class is capable of getting are dairy imports, dairy exports, and casein exports.

## Usage
* You need to specify the time period for which you wish to get data for, and also the specific data you wish to get (dairy imports, dairy exports, or casein trade).
* Example 1: get data on dairy imports from Januray 2015 to January 2019
```python
Statsnz().scrape(start_date="2015M01", end_date="2019M01", desired_stats="dairy_imports")
```

* Example 2: get data on casein trade for July 2019
```python
Statsnz().scrape(start_date="2019M07", end_date="2019M07", desired_stats="casein_trade")
```

## Notes
* Dates have to be in the format from above, i.e.: `"2019M07"`
* The date range is 1988-current year
* The three keywords for `desired_stats` are: `"dairy_imports"`, `"dairy_exports"`, `"casein_trade"`
* File names are in the format: `datetime + "_" + desired_data + "_" + start_date + "-" + end_date + ".csv"` Example: `2019-07-13_00-21-16_casein_trade_2018M01-2019M02.csv`
* The data is limited to 100,000 cells on the website, meaning the datasets are limited. However, I solved this problem by implementing a way to concatenate multiple files into one. The data is concatenated horizontally, meaning that data from new files is added to the right side of the previous data. Like so:
```
             # File 1              # File 2
__________________________________ ______________________
            | Column 1 | Column 2 | Column 1 | Column 2 |
Ireland     | -        | -        | -        | -        |
Slovakia    | -        | -        | -        | -        |
```
