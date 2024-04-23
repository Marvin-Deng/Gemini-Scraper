import unittest
from gemini.link_extractor import get_base_url, get_relevant_links, extract_links


class TestGetBaseUrl(unittest.TestCase):

    def test_base_https_url(self):
        url = "https://www.example.com"
        self.assertEqual(get_base_url(url), "https://www.example.com")

    def test_http_url_with_path(self):
        url = "http://www.example.com/path/?query=123"
        self.assertEqual(get_base_url(url), "http://www.example.com")

    def test_ftp_url(self):
        url = "ftp://ftp.example.com/directory/file.txt"
        self.assertEqual(get_base_url(url), "ftp://ftp.example.com")

    def test_url_with_subdomain(self):
        url = "https://subdomain.example.com"
        self.assertEqual(get_base_url(url), "https://subdomain.example.com")


class TestExtractLinks(unittest.TestCase):
    def test_extract_links_with_absolute_urls(self):
        html_source = '<html><body><a href="https://www.link1.com">Link 1</a><a href="https://www.link2.com">Link 2</a></body></html>'
        base_url = ""
        expected_links = [
            {"url": "https://www.link1.com", "text": "Link 1"},
            {"url": "https://www.link2.com", "text": "Link 2"},
        ]
        self.assertEqual(extract_links(base_url, html_source), expected_links)

    def test_extract_links_with_relative_urls(self):
        html_source = '<html><body><p><a href="/path/to/page">Link 1</a></p><ul><li><a href="/path/to/page?query=123">Link 2</a></li></ul></body></html>'
        base_url = "https://www.link.com"
        expected_links = [
            {"url": "https://www.link.com/path/to/page", "text": "Link 1"},
            {"url": "https://www.link.com/path/to/page?query=123", "text": "Link 2"},
        ]
        self.assertEqual(extract_links(base_url, html_source), expected_links)

    def test_link_text_stripping(self):
        html = '<a href="https://example.com">   Visit   </a>'
        base_url = "https://example.com"
        expected = [{"url": "https://example.com", "text": "Visit"}]
        result = extract_links(base_url, html)
        self.assertEqual(result, expected)

    def test_handles_special_characters_in_links(self):
        html = '<a href="/search?query=hello*world">Search</a>'
        base_url = "https://example.com"
        expected = [
            {"url": "https://example.com/search?query=hello*world", "text": "Search"}
        ]
        result = extract_links(base_url, html)
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        html = """
        <a href="https://example.com/page1">Page 1</a>
        <a href="https://example.com/page2">Page 2</a>
        """
        base_url = "https://example.com"
        expected = [
            {"url": "https://example.com/page1", "text": "Page 1"},
            {"url": "https://example.com/page2", "text": "Page 2"},
        ]
        result = extract_links(base_url, html)
        self.assertEqual(result, expected)

    def test_empty_html_with_no_links(self):
        html_source = ""
        base_url = ""
        expected_links = []
        self.assertEqual(extract_links(base_url, html_source), expected_links)


if __name__ == "__main__":
    unittest.main()
