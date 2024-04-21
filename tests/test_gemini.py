import unittest
from gemini.link_extractor import get_relevant_links, extract_links


class TestExtractLinks(unittest.TestCase):
    def test_extract_links(self):
        html_source = '<html><body><a href="https://www.link1.com">Link 1</a><a href="https://www.link2.com">Link 2</a></body></html>'
        expected_links = ["https://www.link1.com", "https://www.link2.com"]
        self.assertEqual(extract_links(html_source), expected_links)

    def test_multiple_links_nested(self):
        html_source = '<html><body><p><a href="https://www.link1.com">Link 1</a></p><ul><li><a href="https://www.link2.com">Link 2</a></li><li><a href="https://www.link3.com">Link 3</a></li></ul></body></html>'
        expected_links = [
            "https://www.link1.com",
            "https://www.link2.com",
            "https://www.link3.com",
        ]
        self.assertEqual(extract_links(html_source), expected_links)

    def test_empty_html_with_no_links(self):
        html_source = ""
        expected_links = []
        self.assertEqual(extract_links(html_source), expected_links)


class TestSearchForLinks(unittest.TestCase):

    def test_search_for_links_invalid_input(self):
        html_source = ""
        topics = ["Wikipedia"]
        response = get_relevant_links(html_source, topics)
        self.assertIsInstance(response, str)
        self.assertEqual("None", response)

    def test_search_for_links_no_topics(self):
        html_source = "<html><body><a href='https://www.wikipedia.org/'>Wikipedia</a></body></html>"
        topics = []
        response = get_relevant_links(html_source, topics)
        self.assertIsInstance(response, str)
        self.assertEqual("None", response)

    def test_search_for_links_multiple_topics(self):
        html_source = "<html><body><a href='https://www.wikipedia.org/'>Wikipedia</a><a href='https://www.google.com/'>Google</a></body></html>"
        topics = ["Wikipedia", "Google"]
        response = get_relevant_links(html_source, topics)
        self.assertIsInstance(response, str)
        self.assertIn("https://www.google.com/", response)

    def test_search_for_links_multiple_links_same_topic(self):
        html_source = "<html><body><a href='https://www.wikipedia.org/'>Wikipedia</a><a href='https://en.wikipedia.org/'>English Wikipedia</a></body></html>"
        topics = ["Wikipedia"]
        response = get_relevant_links(html_source, topics)
        self.assertIsInstance(response, str)
        self.assertIn("https://www.wikipedia.org/", response)


if __name__ == "__main__":
    unittest.main()
