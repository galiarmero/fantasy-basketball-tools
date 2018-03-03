from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import getpass

from yahoo_auth import YahooAuth

YAHOO_FANTASY_URL = "https://basketball.fantasysports.yahoo.com"

class YahooFantasy(object):
    def __init__(self, driver):
        self._driver = driver
        self._yahoo_auth = YahooAuth(self._driver, YAHOO_FANTASY_URL)

    def go_to_league(self, league_name=None, league_id=None):
        self._login()
        self._click_league(league_name, league_id)

    def _login(self):
        username = input("Enter Yahoo email: ")
        password = getpass.getpass(prompt="Enter Yahoo password: ")
        self._yahoo_auth.login(username, password)

    def _click_league(self, league_name, league_id):
        LEAGUE_PARENT = "*[@id='gamehome-teams']/h3"
        if league_name:
            a_xpath = "//{}/a[.='{}']".format(LEAGUE_PARENT, league_name)
        elif league_id:
            a_xpath = "//{}/a[contains(@href,'{}')]".format(LEAGUE_PARENT, league_id)
        else:
            a_xpath = "//{}/a[1]".format(LEAGUE_PARENT)

        try:
            league_link = self._driver.find_element_by_xpath(a_xpath)
            league_link.click()
        except NoSuchElementException:
            print("League not found")

        print(league_name in self._driver.page_source)

        if league_id:
            try:
                self._wait.until(expect.url_contains(league_id))
            except TimeoutException:
                print("Invalid url")
            

        