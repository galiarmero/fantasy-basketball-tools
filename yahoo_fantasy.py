from selenium import webdriver
import getpass

from config import headless_chrome_options
from yahoo_auth import YahooAuth

YAHOO_FANTASY_URL = "https://basketball.fantasysports.yahoo.com"

class YahooFantasy(object):
    def __init__(self):
        self._driver = webdriver.Chrome(chrome_options=headless_chrome_options)
        self._yahoo_auth = YahooAuth(self._driver, YAHOO_FANTASY_URL)

    def go_to_league(self, league):
        username = input("Enter Yahoo email: ")
        password = getpass.getpass(prompt="Enter Yahoo password: ")
        self._yahoo_auth.login(username, password)

if __name__ == "__main__":
    yf = YahooFantasy()
    yf.go_to_league('PogiLig 2017-18')