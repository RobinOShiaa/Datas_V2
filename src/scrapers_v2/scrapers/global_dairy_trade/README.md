# Documentation
## Purpose
Scrapes the event number, date, GDT price index, average price, and products from [globaldairytrade](https://www.globaldairytrade.info/en/product-results/). Stores the data in a `csv` file.

## Usage
* No special user input is possible here. Example:
```python
GlobalDairyTrade().scrape()
```

## Notes
The `is_number()` method checks whether a valid sum of money is present. For example, are `$375`, `$3,785`, and `n.a.` valid sums of money? The method has a small list of currency symbols (GBP, USD, EUR, YEN) used during the check, even though the website uses USD. I added the list in order to reduce the possibility of an `Exception` occuring when a different currency would be used other than USD.
