import functools
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class YahooAuth(object):
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 90)

    @classmethod
    def ensures_login(this, target_url):
        def login_then_execute(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                driver = args[0]._driver
                self = this(driver)
                full_target_url = urljoin(target_url, str(args[1]))

                try:
                    self._login(full_target_url)
                    print("Login successful")
                except TimeoutException:
                    print("Failed to login within 90 secs\nClosing browser")
                return func(*args, **kwargs)
            return wrapper
        return login_then_execute


    def _login(self, target_url="https://www.yahoo.com"):
        print("Attempting login")
        self._driver.get(target_url)
        self._wait.until(expect.url_contains(target_url))

    
    def _enter_username(self, username):
        username_input = self._wait.until(
            expect.presence_of_element_located(
                (By.ID, "login-username"))
        )
        username_input.send_keys(username)

        next_button = self._wait.until(
            expect.element_to_be_clickable(
                (By.ID, "login-signin"))
        )
        next_button.click()

        try:
            self._wait.until(expect.url_contains("/account/challenge/password"))
            print("Username is recognized.")
        except TimeoutException:
            try:
                self._driver.find_element_by_xpath(
                    "//p[@id='username-error' and @data-error='messages.ERROR_INVALID_USERNAME']")
                print("Username is not recognized. Exiting.")
                exit(1)
            except NoSuchElementException:
                print("An error occurred after entering username.")
                exit(1)


    def _enter_password(self, password):
        password_input = self._wait.until(
            expect.presence_of_element_located(
                (By.ID, "login-passwd"))
        )
        password_input.send_keys(password)

        sign_in_button = self._wait.until(
            expect.element_to_be_clickable(
                (By.ID, "login-signin"))
        )
        sign_in_button.click()

        try:
            self._wait.until(self._url_starts_with_target)
            print("Login successful.")
        except TimeoutException:
            try:
                self._driver.find_element_by_xpath(
                    "//p[contains(concat(' ', @class, ' '), ' error-msg ') and @data-error='messages.ERROR_INVALID_PASSWORD']")
                print("Password is invalid. Exiting.")
                exit(1)
            except NoSuchElementException:
                print("An error occurred after entering password.")
    

    def _url_starts_with_target(self, driver):
        # TODO: Get a hold of target_url somehow
        target_url = "there's a TODO here"
        return driver.current_url and driver.current_url.startswith(target_url)