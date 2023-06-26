# CronometerPy

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python Library for generating json for importing to [Cronometer](https://cronometer.com/) all the CIQUAL table.

Download the [Ciqual table](https://ciqual.anses.fr/cms/sites/default/files/inline-files/Table%20Ciqual%202020_FR_2020%2007%2007.xls) and save it as xlsx format.

Then, run the script [read_ciqual_xlsx.py](https://github.com/LoanSarazin/cronometer-ciqual/blob/main/src/read_ciqual_xlsx.py) and give:

- The absolute path of the xlsx file downloaded previously
- Your Cronometer username (email address)
- Your Cronometer password
- The owner id. You can find it when exporting a custom food to json.
And let it run !

As a test, you can give the file [test_ciqual_table.xlsx](https://github.com/LoanSarazin/cronometer-ciqual/blob/main/src/test_ciqual_table.xlsx) and check on your custom food list if it has been added. Don't forget to refresh the page in order to see it.

Go make something fancy!
