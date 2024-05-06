from crawler.scraper import Scraper
from gemini.analyze_content import gemini_analyze_topics
from gemini.link_extractor import get_relevant_links
from crawler.crawler import Crawler


def main():

    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    topics = ['Early days of the company', 'List of products', 'Important people in the company']
    max_depth = 3

    crawler = Crawler(url, topics, max_depth)
    print(crawler.bfs_crawl())


if __name__ == "__main__":
    main()
