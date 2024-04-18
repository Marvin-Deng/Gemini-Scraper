from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

def wait_elements_visible_by_css(css_selector: str, driver: WebDriver) -> list:
    """
    Wait for all elements matching the CSS selector to be visible and return them.

    Parameters:
    css_selector (str): CSS selector for the elements.
    driver (WebDriver): The WebDriver instance.

    Returns:
    list: List of WebElement instances that are visible.
    """
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )

def wait_element_visible_by_id(element_id: str, driver: WebDriver) -> object:
    """
    Wait for the element with the specified ID to be visible and return it.

    Parameters:
    element_id (str): ID of the element.
    driver (WebDriver): The WebDriver instance.

    Returns:
    WebElement: The WebElement instance that is visible.
    """
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )
