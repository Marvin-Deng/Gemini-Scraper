from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

def wait_elements_visible_by_css(css_selector: str, driver: WebDriver) -> list:
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )

def wait_element_clickable_by_css(css_selector: str, driver: WebDriver) -> None:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    ).click()

def wait_element_clickable_by_id(element_id: str, driver: WebDriver) -> None:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, element_id))
    ).click()