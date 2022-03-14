# scrapers_v2

## Important (Linux)
To get the path to the `csv_files` directory working from the unit tests, you have to do the following:
1. Open a Terminal and paste in: `gedit ~/.profile`
2. Paste this line at the end of the file: `export CSV_UNIT_TEST_PATH="/home/$USER/csv_files"`
3. Save the file (CTRL + S)
4. Log out of your account

* When initialising an object, supply the path like: `ObjectName(CSV_FOLDER_PATH=os.environ.get("CSV_UNIT_TEST_PATH"))`

![classes](https://i.imgur.com/eZCuV8z.png)
