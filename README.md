# MATRYOSHKA 

Scrape data from the website. Make calculations. Store the result in Google Spreadsheet. 

### Script uses:

- Scrapy 
- Gspread for authorization in Google SpreadSheets

## Getting Started

1. Create Google SpreadSheet

2. In SpreadSheet:
   - Create 2 tabs called 'matr', 'daily'.
   - In 'matr' tab: Add headers in the first row: A - 'Date/Time', V - 'Cost', W - 'Amount' 
   - In the first column of 'matr' tab write today's date and time, i.e. '09.01 12:00'
   - In 'daily' tab: Add headers in the first row: A - 'Date/Time', G - 'Matryoshka'' 
   - In the first column of 'daily' tab write yesterday's date, i.e. '08.01.18'


3. 
```
git clone <...> 
cd matryoshka
```

4. Get Google API credentials for Gspread authorize. 
(Follow https://gspread.readthedocs.io/en/latest/oauth2.html)
Save JSON file with credentials in the current directory.

5. Fill in tokens_example.py file. Rename it to 'tokens.py'.

6. Run script

```
chmod 777 matryoshka_daily.sh
bash matryoshka_daily.py
```
