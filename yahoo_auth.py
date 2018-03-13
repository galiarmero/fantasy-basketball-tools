import sys
import pickle
import functools
from getpass import getpass
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class YahooAuth(object):
    def __init__(self, driver):
        self._driver = driver
        self._wait_login = WebDriverWait(self._driver, 180)
        self._wait = WebDriverWait(self._driver, 10)

    @classmethod
    def ensures_login(this, target_url="https://www.yahoo.com"):
        def login_then_execute(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                driver = args[0]._driver
                self = this(driver)

                full_target_url = target_url.format(*tuple(args[1:]))
                try:
                    self._login(full_target_url)
                    print("Login successful")
                except TimeoutException:
                    print("Failed to login within 90 secs\nClosing browser")
                    driver.close()
                    sys.exit()
                
                return func(*args, **kwargs)
            return wrapper
        return login_then_execute


    def _login(self, target_url):
        print("Attempting login")
        self._driver.get(target_url)
        try:
            self._load_cookies(target_url)
        except (FileNotFoundError, WebDriverException, TimeoutException):
            print("Please manually type your credentials")
            self._wait_login.until(expect.url_contains(target_url))
            self._dump_cookies(target_url)

    def _load_cookies(self, target_url):
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            self._driver.add_cookie(cookie)
        
        self._driver.get(target_url)
        self._wait.until(expect.url_contains(target_url))

    def _dump_cookies(self, target_url):
        pickle.dump(self._driver.get_cookies(), open("cookies.pkl", "wb"))
