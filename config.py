from selenium.webdriver.chrome.options import Options

headless_chrome_options = Options()
headless_chrome_options.add_argument("--headless")
headless_chrome_options.add_argument("--disable-gpu")