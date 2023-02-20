BASE_URL = "https://aktie.traderfox.com/"

ELEMENTS = {
    'cookies_button': '//*[@id="tfcookie-accept-all"]',
    'search_bar': '//*[@id="form_search"]/div[2]/input',
    'search_button': '//*[@id="submit_search"]',
    'quality_tab': '//*[@id="tdf-quality-check-tab"]',
    'dividend_tab': '//*[@id="tdf-dividend-check-tab"]',
    'growth_tab': '//*[@id="tdf-growth-check-tab"]',
    'robustness_tab': '//*[@id="tdf-the_big_call-check-tab"]'
}

TICKER_DIR = "utils/constants/ticker_symbols.py"

TICKERS = [
    'PEP',
    'KO',
    'AAPL',
]