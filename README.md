# Gemini Scraper

## Setup

1. Clone the repo
```shell
git clone https://github.com/Marvin-Deng/Gemini-Scraper.git
cd Gemini-Scraper
```

2. Create a virtual environment
```shell
python -m venv venv

or

python3 -m venv venv
```

3. Start the virtual environment
```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate
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
python main.py

or 

python3 main.py
```

## Updating requirements

```shell
pip freeze > requirements.txt
```
