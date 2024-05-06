import json
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import concurrent.futures

from model import configure_gemini

model = configure_gemini()


def __get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def __extract_links(base_url: str, html_source: str) -> list:
    """
    Extracts links from the given HTML source and returns a list with the link text and absolute URLs.

    Args:
        html_source (str): The HTML source to extract links from.
        base_url (str): The base URL to resolve relative links.

    Returns:
        list: A list of extracted links with their texts and URLs.
    """
    soup = BeautifulSoup(html_source, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        link_text = link.text.strip()
        if href and not href.lower().endswith(
            (".jpg", ".jpeg", ".png", ".gif", ".bmp")
        ):
            absolute_url = (
                urljoin(base_url, href)
                if not href.startswith(("http:", "https:"))
                else href
            )
            links.append({"url": absolute_url, "text": link_text})
    return links


def __get_link_chunks(links: list, chunk_size: int) -> list:
    """
    Splits the given list of links into chunks of a specified size.

    Args:
        links (list): The list of links and text to split into chunks.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of link chunks with the related text.
    """
    chunks = []
    current_chunk = ""
    for link in links:
        url, text = link["url"], link["text"]
        link_string = f"{text}: {url}"
        if len(current_chunk) + len(link_string) + 2 > chunk_size:
            chunks.append(current_chunk.rstrip(", "))
            current_chunk = link_string + ", "
        else:
            current_chunk += link_string + ", "
    if current_chunk:
        chunks.append(current_chunk.rstrip(", "))
    return chunks


def __process_chunk(chunk, topics):
    try:
        prompt = f"""
            Analyze the provided links and topics, and advise on only the most relevant links about each topic. 
            Topics: {', '.join(topics)}. Links: {chunk}.
            Respond with a JSON object containing the recommended links for each topic. 
            Don't include the JSON header.
            Only return the urls. DO NOT include the text related to the url. 
            Only return the 3 most relevant urls to each topic. If there are no relevant links found for the topic, return ""
            Include a space between each link.
        """.strip()
        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception:
        return {}


def __unify_json_objects(main_json: dict, chunk: dict) -> None:
    """
    Append items from one JSON-style dictionary (chunk) into another (main_json).

    Args:
        main_json (dict): The main dictionary to which items will be appended to and is modified in-place.
        chunk (dict): A dictionary containing keys and values to be appended into main_json.
    """
    for topic, links in chunk.items():
        if topic and topic not in main_json:
            main_json[topic] = []
        if links:
            main_json[topic].extend(links if isinstance(links, list) else [links])


def get_relevant_links(url: str, html_source: str, topics: list) -> dict:
    """
    Extracts relevant links from the given HTML source based on the provided topics.

    Args:
        html_source (str): The HTML source to extract links from.
        topics (list): The topics to find relevant links for.

    Returns:
        list: A list of relevant links for each topic.
    """
    base_url = __get_base_url(url)
    links_dict = __extract_links(base_url, html_source)
    link_chunks = __get_link_chunks(links_dict, chunk_size=35000)
    topic_links = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(__process_chunk, chunk, topics) for chunk in link_chunks
        ]
        for future in concurrent.futures.as_completed(futures):
            chunk_result = future.result()
            __unify_json_objects(main_json=topic_links, chunk=chunk_result)

    return topic_links


# Testing script
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Apple_Inc."

    html = ""
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    topics = [
        "Early days of the company",
        "List of products",
        "Important people in the company",
    ]
    if html.startswith("http"):
        print("Failed to fetch URL:", html)
    else:
        print(get_relevant_links(url, html, topics))
