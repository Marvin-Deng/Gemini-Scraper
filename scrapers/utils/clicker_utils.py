from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .helper_utils import parse_css_selector
from .wait_utils import (
    wait_elements_visible_by_css,
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

def click_link_by_css(css_selector: str, driver: WebDriver) -> None:
    """Click on a link matching the CSS selector."""
    css_selector = parse_css_selector(css_selector)  # Modify CSS selector if necessary
    try:
        wait_elements_clickable_by_css(css_selector, driver)
    except TimeoutException:
        print(f"Timeout: Link with CSS '{css_selector}' not clickable within the wait time.")
    except NoSuchElementException:
        print(f"Error: Link with CSS '{css_selector}' not found.")
    except Exception as e:
        print(f"Unhandled exception occurred: {str(e)}")  # Catch any other unexpected exceptions


def click_link_by_class(class_name: str, driver: WebDriver) -> None:
    """Click on a link with a specific class."""
    css_selector = f"a.{class_name}"  # Ensure the selector targets <a> elements with the specified class
    try:
        wait_elements_clickable_by_css(css_selector, driver)
    except TimeoutException:
        print(f"Timeout: Link with class '{class_name}' not clickable within the wait time.")
    except NoSuchElementException:
        print(f"Error: Link with class '{class_name}' not found.")

def click_next_button_by_css(css_selector: str, driver: WebDriver) -> None:
    """Click on the first button matching the css."""
    css_selector = parse_css_selector(css_selector)
    try:
        wait_elements_clickable_by_css(css_selector, driver)
    except TimeoutException as e:
        raise Exception(f"Timeout occured while waiting to click button: {e}")
    except Exception as e:
        raise Exception(f"Clicking button failed with error: {e}")

def wait_element_visible_by_id(element_id: str, driver: WebDriver) -> object:
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )