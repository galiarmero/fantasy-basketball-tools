from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class YahooNbaFantasy(object):
    def __init__(self, driver):
        self._driver = driver

    def get_rosters(self):
        pass
            

        