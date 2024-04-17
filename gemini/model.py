import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-pro")


def gemini_analyze_topics(html_text: str, topics: list) -> str:
    try:
        prompt = f"Parse the following HTML text and organize the content into the following topics: {', '.join(topics)}.\n\n{html_text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini returned with error: {e}"
