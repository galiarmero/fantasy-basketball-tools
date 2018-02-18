from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class YahooAuth(object):
    def __init__(self, driver, target_url="https://www.yahoo.com"):
        self._driver = driver
        self._target_url = target_url
        self._wait = WebDriverWait(self._driver, 10)

    def login(self, username, password):
        try:
            self._driver.get(self._target_url)
            self._go_to_sign_in()
            self._enter_username(username)
            self._enter_password(password)
            
        except TimeoutException:
            print("Page redirected to is different from expected.")
            exit(1)
    
    def _go_to_sign_in(self):
        sign_in = self._wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, "//*[@id='yucs-profile']/a[@role='button']/b[.='Sign in']"))
        )
        sign_in.click()
        self._wait.until(expect.url_contains("/config/login"))
        print("Attempting login.")

    
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
        return driver.current_url.startswith(self._target_url)