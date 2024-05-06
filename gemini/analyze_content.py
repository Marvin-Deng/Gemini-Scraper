from bs4 import BeautifulSoup
from bs4.element import Comment
import json
import requests

from gemini.model import configure_gemini


model = configure_gemini()


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
        topic: f"Relevant information about {topic.lower()}." for topic in topics
    }

    formatted_json_example = json.dumps(example_json, indent=4)

    prompt = f"""
    Please analyze the following text and categorize the information according to these topics: {', '.join(topics)}.
    If there are no relevant info found regarding the topic, return "" for that topic.
    For each topic, format the information into a JSON object as shown in this example:
    {formatted_json_example}
    Don't include the JSON header.

    Text to analyze:
    {text_chunk}
    """
    return prompt


def gemini_analyze_topics(url: str, html_source: str, topics: list) -> list:
    content_chunks = split_html_content(html_source, 35000)
    topic_info = []
    for chunk in content_chunks:
        prompt = generate_prompt(topics, chunk)
        response = model.generate_content(prompt)
        if response.text.strip():  # Check if response is not empty
            topic_info.append(json.loads(response.text))
    return {"url": url, "info": topic_info}


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
    topics = [
        "Early days of the company",
        "List of products",
        "Important people in the company",
    ]
    if html_source.startswith("http"):
        print("Failed to fetch URL:", html_source)
    else:
        print(gemini_analyze_topics(url, html_source, topics))
