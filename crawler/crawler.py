from collections import deque
import threading

from gemini.analyze_content import gemini_analyze_topics
from gemini.link_extractor import get_relevant_links
from crawler.utils.soup_utils import get_html_from_url
from concurrent.futures import ThreadPoolExecutor, as_completed


class Crawler:

    def __init__(self, start_url: str, topics: list, max_depth: int):
        self.lock = threading.Lock()
        self.queue = deque([start_url])
        self.visited = set([start_url])
        self.topics = topics
        self.curr_depth = max_depth

    def extract_data_and_urls(self, url: str):
        """
        Analyzes the content of a URL to extract data related to specified topics and discover new URLs.

        Args:
            url (str): The URL to process.

        Returns:
            tuple: A tuple analyzed topics.
            dict: A dicitonary of URLs categorized by topic.
        """
        # print(f"Extracting URL: {url}")
        try:
            html_source = get_html_from_url(url)
            analyzed_topics = gemini_analyze_topics(html_source, self.topics)
            topic_url_dict = get_relevant_links(url, html_source, self.topics)
            # print(f"Processed: {url}, Links found: {len(topic_url_dict)}")
            return analyzed_topics, topic_url_dict
        except Exception as e:
            # print(f"Error processing URL {url}: {e}")
            return "", {}

    def bfs_crawl(self) -> list:
        """
        Executes a BFS search through a webpage, processing URLs and collecting data until
        the specified maximum depth is reached or there are no more URLs to process.

        Returns:
            list: A list of data collected from each processed URL.
        """
        info = []
        with ThreadPoolExecutor() as executor:
            while self.queue and self.curr_depth > 0:
                # print(f"Processing level {self.curr_depth} with {len(self.queue)} URLs")
                futures = []
                current_level_urls = list(self.queue)
                self.queue.clear()

                # Split the processing of each url to a different thread
                for curr_url in current_level_urls:
                    futures.append(
                        executor.submit(self.extract_data_and_urls, curr_url)
                    )

                # Loop through completed futures to gather page info and next urls
                for future in as_completed(futures):
                    analyzed_topics, topic_url_dict = future.result()
                    if analyzed_topics:
                        info.append(analyzed_topics)
                    for topic, urls in topic_url_dict.items():
                        for url in urls:
                            if url not in self.visited:
                                if url not in self.visited:
                                    self.queue.append(url)
                                    self.visited.add(url)
                self.curr_depth -= 1

        return info
