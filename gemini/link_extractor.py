import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def extract_links(html_source: str) -> str:
    soup = BeautifulSoup(html_source, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None:
            individual_hrefs = re.split(
                r"https?://", href
            )  # Split links that are appended together
            for link in individual_hrefs:
                links.append(link)
    return links


def get_link_chunks(links: list, chunk_size: int) -> list:
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


def get_relevant_links(html_source: str, topics: list) -> list:
    links = extract_links(html_source)
    link_chunks = get_link_chunks(links, chunk_size=35000)
    print(link_chunks)
    result = []
    for chunk in link_chunks:
        try:
            prompt = f"""
                        Analyze the provided links and topics, and advise on which links to click next to find relevant information about each topic. 
                        Topics: {', '.join(topics)}. Links: {chunk}. 
                        Please respond with a JSON object containing the recommended links for each topic. 
                        If no links are found, return ""
                      """
            response = model.generate_content(prompt)
            print(response.text)
            result.append(response.text)
        except Exception as e:
            return f"Gemini returned with the following error: {e}"
    return result
