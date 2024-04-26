from crawler.scraper import Scraper
from gemini.analyze_content import gemini_analyze_topics
from gemini.link_extractor import get_relevant_links


def main():
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    scraper = Scraper(url)

    html = scraper.get_page_source()
    topics = ['Early days of the company', 'List of products', 'Important people in the company']

    # gemini_analyze_topics(html, topics)

    print(get_relevant_links(url, html, topics))

    scraper.close_driver()

if __name__ == "__main__":
    main()
