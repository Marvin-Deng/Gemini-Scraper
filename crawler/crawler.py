from collections import deque

from gemini.analyze_content import gemini_analyze_topics
from gemini.link_extractor import get_relevant_links
from crawler.utils.soup_utils import get_html_from_url
from concurrent.futures import ThreadPoolExecutor, as_completed


class Crawler:

    def __init__(self, start_url: str, topics: list, max_depth: int):
        self.queue = deque([start_url])
        self.visited = set()
        self.topics = topics
        self.curr_depth = max_depth
        self.info = []

    def extract_data_and_urls(self, url):
        print(f"Extracted url: {url}")
        try:
            html_source = get_html_from_url(url)
            # analyzed_topics = gemini_analyze_topics(html_source, self.topics)
            analyzed_topics = "temp info"
            topic_url_dict = get_relevant_links(url, html_source, self.topics)
            return analyzed_topics, topic_url_dict
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return None, {}

    def bfs_crawl(self) -> list:
        with ThreadPoolExecutor() as executor:
            try:
                while self.queue and self.curr_depth > 0:
                    print(self.curr_depth)
                    futures = []

                    # Concurrently process each page in the current level
                    for _ in range(len(self.queue)):
                        curr_url = self.queue.popleft()
                        if curr_url not in self.visited:
                            self.visited.add(curr_url)
                            futures.append(
                                executor.submit(self.extract_data_and_urls, curr_url)
                            )

                    # Wait for all futures to complete before storing results and next urls
                    for future in as_completed(futures):
                        analyzed_topics, topic_url_dict = future.result()
                        if analyzed_topics:
                            self.info.append(analyzed_topics)
                        for topic, urls in topic_url_dict.items():
                            for url in urls:
                                if url not in self.visited:
                                    self.queue.append(url)
                                    self.visited.add(url)
                    self.curr_depth -= 1
            except Exception as e:
                print(f"Error during BFS crawl: {e}")
        return self.info
