# Documentation
## Name changes of `py` files
Original | New
-------- | ---
consumption | eu_per_capita_consumption
slaughtering | eu_weekly_pig_slaughterings_historical
weaner_price | average_weaner_price

## General notes
All `py` files here can be executed simply by calling the `scrape()` method. Some of the `weekly` scripts' `scrape()` method takes an optional `duration` argument which stands for the duration in years. This has to be one of: 0.5, 1, 3, or 5. This is so because some of the webpages allow you to select a duration before downloading the Excel spreadsheet of data. Where a `duration` exists, it will appear in the name of the `csv` output file.

## Usage
```python
AnnualCleanPigSlaughteringsHistorical().scrape()
AnnualCullSowSlaughteringsHistorical().scrape()
WeeklyCleanPigSlaughteringsHistorical().scrape()
WeeklyCullSowSlaughteringsHistorical().scrape()
EuWeeklyPigSlaughteringsHistorical().scrape()
EuPerCapitaConsumption().scrape()
AverageWeanerPrice().scrape()
```
