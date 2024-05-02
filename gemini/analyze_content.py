import os
from bs4 import BeautifulSoup
from bs4.element import Comment
from dotenv import load_dotenv
import google.generativeai as genai
import json
import requests


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def split_html_content(html_source: str, chunk_size: int) -> list:
    soup = BeautifulSoup(html_source, "html.parser")
    text = soup.find_all(string=True) 
    visible_text = filter(tag_visible, text)
    html_content = " ".join(t.strip() for t in visible_text)
    return [
        html_content[i : i + chunk_size]
        for i in range(0, len(html_content), chunk_size)
    ]

def generate_prompt(topics, text_chunk):
    example_json = {
        topics[0]: "Relevant information about topic one.",
        topics[1]: "Relevant information about topic two.",
        topics[2]: "Relevant information about topic three."
    }
    return f"""
    Please analyze the following text and categorize the information according to these topics: {', '.join(topics)}.
    For each topic, format the information in JSON as shown in this example: {json.dumps(example_json, indent=2)}.

    Text to analyze:
    {text_chunk}
    """

def gemini_analyze_topics(html_source: str, topics: list) -> str:
    content_chunks = split_html_content(html_source, 35000)
    results = []
    for chunk in content_chunks:
        prompt = generate_prompt(topics, chunk)
        response = model.generate_content(prompt)
        results.append(response.text)
        if response.text.strip():
            try:
                results.append(response.text)
            except Exception as e:
                results.append("Error processing the chunk")
        else:
            results.append("Empty or invalid response")
    return results


def fetch_html(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        return str(e)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    html_source = fetch_html(url)
    topics = ['Early days of the company', 'List of products', 'Important people in the company']
    if html_source.startswith("http"):
        print("Failed to fetch URL:", html_source)
    else:
        print(gemini_analyze_topics(html_source, topics))