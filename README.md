# Sentiment Analysis Application

This is a simple sentiment analysis application built with FastAPI, aiohttp, and SQLAlchemy. The application has two main components: an API for interacting with a sentiment analysis model and a separate database API for storing and retrieving sentiment analysis results.

## Project Structure

```bash
.
├── .gitignore
├── app/
│   ├── Dockerfile
│   ├── ai.py
│   ├── main.py
│   ├── requirements.txt
│   └── templates/
│       ├── error.html
│       ├── form.html
│       └── results.html
├── database/
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 2b2d05612323_create_sentiments_table.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── test.db
├── schemas/
│   ├── __init__.py
│   └── sentiment_schemas.py
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## How does application works

The application will be available at http://localhost:8080.

The database API will be available at http://localhost:8081.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SHASHA184/text_sentimentor
```

2. Change into the project directory:

```bash
cd text_sentimentor
```

3. Run the following command to build and start the application:

```bash
docker-compose up
```

4. Open your browser and navigate to `http://localhost:8080` to access the application.

5. To stop the application, run the following command:

```bash
docker-compose down
```

## Usage

To use the application, enter a text in the input field and click the "Analyze" button. The application will display the sentiment of the text as either "Positive", "Negative", or "Neutral" and other information.
