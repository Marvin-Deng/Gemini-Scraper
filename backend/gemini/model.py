from dotenv import load_dotenv
import os
import google.generativeai as genai


def configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    return model
