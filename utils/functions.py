from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.constants.arguments import BASE_URL, ELEMENTS
import pandas as pd
import time
from utils.constants.arguments import TICKER_DIR
import gspread as gs
from gspread_pandas import Spread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

spreadsheet_id = os.getenv("SPREADSHEET_ID")
ticker_worksheet = os.getenv("TICKER_WORKSHEET")
results_worksheet = os.getenv("RESULTS_WORKSHEET")
json_credentials_dir = os.getenv("JSON_CREDENTIALS_DIR")

def initiate_google():
    gc = gs.service_account(json_credentials_dir)
    spreadsheet = gc.open_by_key(spreadsheet_id)
    return spreadsheet

def clear_previous():
    spreadsheet = initiate_google()
    worksheet = spreadsheet.worksheet(results_worksheet)
    worksheet.batch_clear(["A:G"])

def get_ticker_symbols():
    spreadsheet = initiate_google()
    worksheet = spreadsheet.worksheet(ticker_worksheet)
    rows = worksheet.get_all_records()
    df = pd.DataFrame(rows)
    index_list = df[df['Ticker Symbols to Scrape'] == ''].index
    df = df.drop(index_list)
    ticker_symbols = df['Ticker Symbols to Scrape'].tolist()
    
    with open(TICKER_DIR, 'w') as f:
        f.write(f"TICKERS = {ticker_symbols}")

def initiate_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def access_stock_url(driver, new_row, ticker):
    driver.delete_all_cookies()
    driver.get(BASE_URL)
    
    # Accept cookies
    WebDriverWait(driver, 20) \
        .until(EC.element_to_be_clickable((By.XPATH, ELEMENTS['cookies_button']))).click()

    # Enter stock ticker symbol into search bar and go
    WebDriverWait(driver, 20) \
        .until(EC.presence_of_element_located((By.XPATH, ELEMENTS['search_bar']))) \
        .send_keys(ticker)
    WebDriverWait(driver, 20) \
        .until(EC.presence_of_element_located((By.XPATH, ELEMENTS['search_button']))) \
        .click()
    time.sleep(5)
    return driver, new_row

def get_score(driver, new_row, tab_idx):
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html5lib")
    scores = soup.find_all("div", {"class":"col-3 col-lg-2 order-1 order-lg-5 text-center border-l border-color-grey p-0 d-flex flex-column line-height-100"})
    inner_span = scores[tab_idx].find("span", {"class": "flex-grow-1 d-flex flex-column justify-content-center color-white pb-2 pt-1 px-2 px-xl-3 fs-300"})
    if inner_span:
        score_span = inner_span.find("span")
        
        score_text = score_span.text.strip()  # Get the text and strip it
        # print('score_text:', score_text)
        if "/" in score_text:  # If it's in the form '13/15'
            extracted_score = score_text.split("/")[0]  # Extract the first part (13)
    else:
        extracted_score = 'N/A'
    print('extracted_score:', extracted_score)
    new_row.append(extracted_score)
    return driver, new_row

def iterate_through_tabs(driver, new_row):
    tabs = list(ELEMENTS.values())[3:]
    for tab_idx, tab in enumerate(tabs):
        print('TAB', list(ELEMENTS.keys())[list(ELEMENTS.values()).index(tab)])
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, tab))).click()
        time.sleep(5)
        driver, new_row = get_score(driver, new_row, tab_idx)
    print('new_row', new_row)
    
    return driver, new_row

def update_gsheet(df: pd.DataFrame):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_credentials_dir, scopes=scope)
    spread = Spread(spreadsheet_id, creds=credentials)
    spread.df_to_sheet(df, sheet=results_worksheet)