import os
from bs4 import BeautifulSoup
from bs4.element import Comment
from dotenv import load_dotenv
import google.generativeai as genai

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
    text = soup.find_all(text=True)
    visible_text = filter(tag_visible, text)
    html_content = " ".join(t.strip() for t in visible_text)
    return [
        html_content[i : i + chunk_size]
        for i in range(0, len(html_content), chunk_size)
    ]


def gemini_analyze_topics(html_source: str, topics: list) -> str:
    content_chunks = split_html_content(html_source, 35000)
    result = []
    for chunk in content_chunks:
        try:
            prompt = f"Parse the following text and organize the content into the following topics: {', '.join(topics)}.\n\n{chunk} \n\n Output should be a a JSON array with each topic corresponsing to the information retrieved. If the information for a topic cannot be found, "
            response = model.generate_content(prompt)
            if hasattr(response, "prompt_feedback"):
                print(
                    f"Prompt was blocked or failed, feedback: {response.prompt_feedback}"
                )
            print(response.text)
            result.append(response.text)
        except Exception as e:
            return f"Gemini returned with the following error: {e}"
    return result
