import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def extract_links(html_source: str) -> list:
    soup = BeautifulSoup(html_source, "html.parser")
    links = []
    for link in soup.find_all("a"):
        links.append(link.get("href"))
    return links


def get_relevant_links(html_source: str, topics: list) -> str:
    links = extract_links(html_source)
    try:
        prompt = f"""Analyze the provided links and topics, and advise on which links to click next to find relevant information about each topic. Topics: {', '.join(topics)}. Links: {', '.join(links)}. 
                    Please respond with a comma separated list of recommended links. 
                    If no links are found, return the string "None"
                    """
        response = model.generate_content(prompt)
    except Exception as e:
        return f"Gemini returned with the following error: {e}"
    return response.text
