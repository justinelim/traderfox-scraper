import pandas as pd
import traceback
from utils.functions import clear_previous, get_ticker_symbols, initiate_driver, access_stock_url, update_gsheet, iterate_through_tabs
# from utils.constants.ticker_symbols import TICKERS  # for testing
import time

df = pd.DataFrame(columns=['refresh_date', 'ticker_symbol', 'quality', 'dividend', 'growth', 'robustness'])  # create empty dataframe
#TODO explore threading to improve scraping speed

def main():
    tic = time.perf_counter()
    clear_previous()
    get_ticker_symbols()
    driver = initiate_driver()
    from utils.constants.ticker_symbols import TICKERS
    print(TICKERS)

    for ticker in TICKERS:
        try:
            print(f'{ticker} scraping started..')
            score_pointer = 0
            new_row = []
            new_row.append(pd.to_datetime('now'))
            new_row.append(ticker)
            driver, score_pointer, new_row = access_stock_url(driver, score_pointer, new_row, ticker)
            driver, score_pointer, new_row = iterate_through_tabs(driver, score_pointer, new_row)
            print(f'{ticker} scraping done! New row created: {new_row}')
            df.loc[len(df.index)] = new_row
        except Exception as e:
            print(e)
            traceback.print_exc()
            #TODO print out the exact stacktrace error and create a row to indicate problematic tickers
    driver.quit()
    update_gsheet(df)
    
    toc = time.perf_counter()
    print(f"Completed job in {toc - tic:0.4f} seconds")

if __name__ == "__main__":
    main()