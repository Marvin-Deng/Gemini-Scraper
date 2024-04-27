from collections import deque

from gemini.analyze_content import gemini_analyze_topics
from gemini.link_extractor import get_relevant_links
from crawler.utils.soup_utils import get_html_from_url

class Crawler:

    def __init__(self, start_url: str, topics: list, max_depth: int):
        self.queue = deque([start_url])
        self.visited = set()
        self.topics = topics
        self.curr_depth = max_depth
        self.info = []

    def bfs_crawl(self) -> list:
        try:
            while self.queue and self.curr_depth > 0:
                for _ in range(len(self.queue)):
                    curr_url = self.queue.popleft()
                    html_source = get_html_from_url(curr_url)
                    # self.info.append(gemini_analyze_topics(html_source, self.topics))
                    topic_url_dict = get_relevant_links(curr_url, html_source, self.topics)
                    for topic, urls in topic_url_dict.items():
                        for url in urls:
                            if url not in self.visited:
                                self.queue.append(url)
                                self.visited.add(url)
                self.curr_depth -= 1
        except Exception as e:
            print(e)
        return self.info
            



