import os
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def extract_links(html_source: str) -> str:
    """
    Extracts links from the given HTML source.

    Args:
        html_source (str): The HTML source to extract links from.

    Returns:
        list: A list of extracted links.
    """
    base_url = "(link unavailable)"
    soup = BeautifulSoup(html_source, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and not href.endswith(".jpg"):
            absolute_url = urljoin(base_url, href).replace("*", "")
            if absolute_url.startswith("http"):
                links.append(absolute_url)
    return links


def get_link_chunks(links: list, chunk_size: int) -> list:
    """
    Splits the given list of links into chunks of a specified size.

    Args:
        links (list): The list of links to split into chunks.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of link chunks.
    """
    chunks = []
    current_chunk = ""
    for link in links:
        if len(current_chunk) + len(link) + 1 > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = link
        else:
            current_chunk += link + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def get_relevant_links(html_source: str, topics: list) -> dict:
    """
    Extracts relevant links from the given HTML source based on the provided topics.

    Args:
        html_source (str): The HTML source to extract links from.
        topics (list): The topics to find relevant links for.

    Returns:
        list: A list of relevant links for each topic.
    """
    links = extract_links(html_source)
    link_chunks = get_link_chunks(links, chunk_size=35000)
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
