from selenium.webdriver.chrome.options import Options
import os

headless_chrome_options = Options()
# headless_chrome_options.add_argument("--headless")
# headless_chrome_options.add_argument("--disable-gpu")


YAHOO_FANTASY_URL = "https://basketball.fantasysports.yahoo.com"
YAHOO_NBA_FANTASY_URL = "https://basketball.fantasysports.yahoo.com/nba/"
CURRENT_SEASON = 2017
DATA_DIR = 'data'