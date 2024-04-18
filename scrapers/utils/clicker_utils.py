from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .helper_utils import parse_css_selector
from .wait_utils import (
    wait_elements_clickable_by_css,
    wait_elements_visible_by_id,
    wait_elements_clickable_by_id,
)

def click_link_by_id(link_id: str, driver: WebDriver) -> None:
    """Click on a link given its ID."""
    try:
        wait_elements_clickable_by_id(link_id, driver)
    except TimeoutException:
        print(f"Timeout: Link with ID '{link_id}' not clickable within the wait time.")
    except NoSuchElementException:
        print(f"Error: Link with ID '{link_id}' not found.")