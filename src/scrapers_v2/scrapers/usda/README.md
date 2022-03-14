# Documentation Part 1: `usda.py`
## Purpose
Uses API calls to get a specific type of output, and writes it to a `csv` file. The following data can be obtained (called `desired_stats`): 

## Usage
* User may specify two inputs. `desired_stats` and `year_range`. The former is the list above, and the latter is a range of years whose data you wish to get.
* Example 1: get data for `pig_crops` for years 2015-2019
```python
Usda().scrape(desired_stats=["pig_crops"], year_range=[2015, 2019])
```

* Example 2: get data for all of the `desired_stats` for the year 2019
```python
Usda().scrape(year_range=[2019, 2019])
```
If you wish to get all of the `desired_stats` then you don't need to supply a list for it.

## Output names explained
The output names are in the following format: `datetime` + `desired_stats` + `year_range` + `.csv`
* Example: `2019-07-10_20-24-27_pig_crops_2017-2019.csv`

## Valid inputs
```
desired_stats: "all_animal_products",
               "dairy_quickstats",
               "dairy_quickstats_cold_storage",
               "hog_slaughters",
               "pig_crops",
               "pork_production_stocks"

year_range:    1915-current_year
```

# Documentation Part 2: `gats.py`
## Purpose
Downloads data from [gats](https://apps.fas.usda.gov/gats/ExpressQuery1.aspx) and writes it to a `csv` file.

## Usage
* Example 1: get exports for casein and dairy for 2016-2019
```python
Gats().scrape(desired_stats=["trade_flow_casein", "trade_flow_dairy"], product_type="exports", year_range=[2016, 2019])
```
* Example 2: get imports for casein for 2019
```python
Gats().scrape(desired_stats=["trade_flow_casein"], product_type="imports - general", year_range=[2019, 2019])
```

## Valid inputs
```
desired_stats: "trade_flow_casein",
               "trade_flow_dairy",
               "trade_flow_meat"

product_type:  "exports",
               "imports - consumption",
               "imports - general",
               "re-exports"

year_range:    1967-current year
```

# Documentation Part 3: `psd.py`
## Purpose
Downloads an Excel readable HTML table from [psd](https://apps.fas.usda.gov/psdonline/app/index.html#/app/advQuery) and stores it in a `csv` file.

## Usage
* Example 1: get dairy data for 2012-2013
```python
Psd().scrape(desired_stats=["dairy"], year_range=[2012, 2013])
```

* Example 2: get data for grains and poultry for 2019
```python
Psd().scrape(desired_stats=["grains", "poultry"], year_range=[2019, 2019])
```

## Valid inputs
```
desired_stats:       "coffee",
                     "cotton",
                     "dairy",
                     "field crops - production",
                     "fruits and vegetables",
                     "grains",
                     "juice",
                     "livestock and poultry",
                     "oilseeds",
                     "poultry",
                     "sugar",
                     "tree nuts"

year_range:          1960-current year + 1
```
