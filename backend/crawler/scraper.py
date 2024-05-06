from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Scraper:

    def __init__(self, url: str):
        self.curr_url = url
        self.driver = Driver(uc=True)

        self.setup_driver()

    def setup_driver(self):
        self.driver.get(self.curr_url)
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.url_to_be(self.curr_url))
        print("Page source obtained successfully!")

    def close_driver(self) -> None:
        if self.driver:
            self.driver.quit()
            print("Driver closed successfully!")

    def get_page_source(self):
        return self.driver.page_source
