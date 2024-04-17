from scrapers.driver import GeminiDriver
from bs4 import BeautifulSoup

def main():
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    driver = GeminiDriver(url)

    if driver:
        driver.quit()

if __name__ == "__main__":
    main()