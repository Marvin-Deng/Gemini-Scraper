# Gemini Scraper

## Setup

1. Clone the repo
```shell
git clone https://github.com/Marvin-Deng/Gemini-Scraper.git
cd Gemini-Scraper
```

2. Create a virtual environment
```shell
python3 -m venv venv
```

3. Start the virtual environment
```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate

# To switch your Python interpreter path
./backend/venv/bin/python
```

4. Install requirements
```shell
pip install -r requirements.txt
```

5. Create a `.env` file in the project root and add your [Google Gemini API key](https://aistudio.google.com/app/apikey)
```shell
# .env
GEMINI_API_KEY=""
```

## Running

```shell
# Start server
uvicorn main:app --reload
```

## Running Tests

```shell
# Timing and response script
python3 tests/test_timing.py

# Unit tests
python -m unittest

# Link extractor script
python3 gemini/link_extractor.py

# Content extractor script
python3 gemini/analyze_content.py
```

## Updating requirements

```shell
pip freeze > requirements.txt
```