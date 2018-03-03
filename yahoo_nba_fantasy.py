from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from yahoo_auth import YahooAuth

YAHOO_FANTASY_URL = "https://basketball.fantasysports.yahoo.com"

class YahooNbaFantasy(object):
    def __init__(self, driver):
        self._driver = driver
        self._yahoo_auth = YahooAuth(self._driver)

    def go_to_league(self, username, password, league_id):
        self._login(username, password, YAHOO_FANTASY_URL + "/nba/" + str(league_id))

    def _login(self, username, password, redirect_url):
        self._yahoo_auth.login(username, password, redirect_url)
            

        