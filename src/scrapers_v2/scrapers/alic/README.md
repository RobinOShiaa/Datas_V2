# Documentation
## Purpose
Scrapes rows that contain Excel files from [alic](http://lin.alic.go.jp/alic/statis/dome/data2/e_nstatis.htm). After scraping is done, it will start downloading the files into `csv_files` folder. Note however, the files downloaded are Excel (`xlsx`) files.

## More info
* Users may specify which categories they wish to scrape. Valid categories are the titles of tables. At the time of writing this code the valid categories were:
```python
["Supply and Demand for Livestock Products", "Meat relation", "Beef and Cattle", "Pork and Hog", "Broiler",
"Milk and Dairy Products", "Egg"]
```

* The list of categories is not case sensitive.

Here you can see what I mean by 'categories':
![screenshot](https://i.imgur.com/nqbNVJK.png)

* `xlsx` file names are created with the combination of `row_name + "_" + column_name + ".xlsx"`. Example: `meats for processing_previous data.xlsx`

## Usage
This class is straight forward to use. You either supply a list of categories to the `scrape()` method, or you don't (in which case everything gets downloaded).

* Example 1: download every Excel file.
```python
Alic().scrape()
```

* Example 2: download Excel files from specified categories.
```python
my_categories = ["Supply and Demand for Livestock Products", "Meat relation", "Beef and Cattle"]
Alic().scrape(my_categories)
```
