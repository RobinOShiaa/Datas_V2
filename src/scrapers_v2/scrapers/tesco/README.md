# Documentation
## Purpose
This class scrapes all of the products from https://www.tesco.ie/groceries/ and stores them in a `csv` file.

## Usage
```python
Tesco().scrape()
```
## Implementation pseudo code
```python
class Tesco(ChromeScraper):
    
    def scrape():
        # Get a dictionary of the navigation menus
        menu_dict = get_menu_dict()

        with open(new_file, encoding="utf-8"):
            for menu in menu_dict:
                for sub_menu in menu_dict[menu].items()
                    # current_products is dictionary of product names, prices, unit prices and units
                    current_products = scrape_products()
                    writer.writerow([category, subcategory, product_name, price, unit_price, unit])

                    # Clicking 'next' page
                    while True:
                        try:
                            next_page.click()
                            current_products = scrape_products()
                            writer.writerow([category, subcategory, product_name, price, unit_price, unit])
                        except ElementNotFound:
                            # We have reached the last page, so 'next' button is not found
                            break

    def scrape_products():
        name_price_dict = dict(zip(product_names, product_prices))
        return name_price_dict

    def get_menu_dict():
        menu_dict = {tag.text: [tag.href] for tag in top_level_menus}
        for menu in menu_dict:
            menu_dict[menu].append(footer_menus)
        hide_images()
        return menu_dict
````
