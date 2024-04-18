from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .helper_utils import parse_css_selector
from .wait_utils import (
    wait_elements_visible_by_css,
    wait_elements_visible_by_id,
    wait_elements_clickable_by_css,
)

def wait_element_visible_by_id(element_id: str, driver: WebDriver) -> object:
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )