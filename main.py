import time

from scrapers.gemini_scraper import GeminiScraper
from gemini.model import gemini_analyze_topics


def main():
    json_format = """
    {
    "topics": str,
    "info": str,
    }
    """

    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    scraper = GeminiScraper(url)

    time.sleep(2)

    html = scraper.get_page_source()
    topics = ['Early days of the company', 'List of products', 'Important people in the company']
    max_depth = 3

    print(gemini_analyze_topics(html, topics))


if __name__ == "__main__":
    main()
