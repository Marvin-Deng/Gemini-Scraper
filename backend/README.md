# Backend

1. Create a virtual environment
```shell
cd backend
python3 -m venv venv
```

2. Start the virtual environment
```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate

# To switch your Python interpreter path
./backend/venv/bin/python
```

3. Install requirements
```shell
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your [Google Gemini API key](https://aistudio.google.com/app/apikey)
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