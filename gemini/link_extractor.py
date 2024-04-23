import os
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def extract_links(base_url: str, html_source: str) -> list:
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
        if href and not href.endswith(".jpg"):
            absolute_url = (
                urljoin(base_url, href)
                if not href.startswith(("http:", "https:"))
                else href
            )
            absolute_url = absolute_url.replace("*", "")
            links.append({"url": absolute_url, "text": link_text})
    return links


def get_link_chunks(links: list, chunk_size: int) -> list:
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


def get_relevant_links(url: str, html_source: str, topics: list) -> dict:
    """
    Extracts relevant links from the given HTML source based on the provided topics.

    Args:
        html_source (str): The HTML source to extract links from.
        topics (list): The topics to find relevant links for.

    Returns:
        list: A list of relevant links for each topic.
    """
    base_url = get_base_url(url)
    links_dict = extract_links(base_url, html_source)
    link_chunks = get_link_chunks(links_dict, chunk_size=35000)
    result = {}
    for chunk in link_chunks:
        try:
            prompt = f"""
                        Analyze the provided links and topics, and advise on only the most relevant links about each topic. 
                        Topics: {', '.join(topics)}. Links: {chunk}. 
                        Respond with a JSON object containing the recommended links for each topic. 
                        Don't include the JSON header
                        If no links are found, return ""
                    """.strip()
            response = model.generate_content(prompt)
            response_json = json.loads(response.text)
            for topic, links in response_json.items():
                if links is not None:
                    if topic not in result:
                        result[topic] = []
                    if isinstance(links, list):
                        result[topic].extend(links)
                    else:
                        result[topic].append(links)
        except Exception:
            pass
    return result
