from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class GeminiDriver:

    def __init__(self, url: str):
        self.driver = Driver(uc=True)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.url_to_be(url))
        print("Page source obtained successfully.")
