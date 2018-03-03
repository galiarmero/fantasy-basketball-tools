from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import getpass

from yahoo_auth import YahooAuth

YAHOO_FANTASY_URL = "https://basketball.fantasysports.yahoo.com"

class YahooNbaFantasy(object):
    def __init__(self, driver):
        self._driver = driver
        self._yahoo_auth = YahooAuth(self._driver)

    def go_to_league(self, league_id):
        self._login(YAHOO_FANTASY_URL + "/nba/" + str(league_id))

    def _login(self, redirect_url):
        username = input("Enter Yahoo email: ")
        password = getpass.getpass(prompt="Enter Yahoo password: ")
        self._yahoo_auth.login(username, password, redirect_url)
            

        