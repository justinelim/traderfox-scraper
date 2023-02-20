# TraderFox Webscraper
This is a script that automates scraping data from a stock analysis website to Google Sheets using the selenium and beautifulsoup4 libraries.

## Usage
1. Follow the steps [here](https://developers.google.com/workspace/guides/create-credentials#service-account) to create your Google service account and credentials
2. Add your service account as an editor to your Google Sheet
3. Create a .env file and declare the following string variables:
- `JSON_CREDENTIALS_DIR` - the local directory in which you store your json credentials
- `SPREADSHEET_ID` - the long string trailing behind your Google Sheet URL
- `TICKER_WORKSHEET` - worksheet where you manually input the ticker symbols of companies of interest
- `RESULTS_WORKSHEET` - worksheet where the webscraping results will be written
4. To run the script, use the following command:

```bash
python main.py
```
The script retrieves ticker symbols from a Google Sheet, and scrapes associated data from the following website: https://aktie.traderfox.com/. The data scraped will be the quality, dividend, growth & robustness scores assigned by the website to each company. The output will be printed to another worksheet in the Google Sheet.

## Future Work
- Current processing speed hovers around 15 min for about 20 tickers. To improve this, I'd like to parallelize the processing of the ticker requests, rather than have them run in a linear fashion.