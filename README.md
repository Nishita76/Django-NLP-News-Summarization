# Django-NLP-News-Summarization
This project is a web-based solution for summarizing news articles using advanced Natural Language Processing (NLP) techniques. The project is implemented using the Django web framework, integrated with Hugging Face Transformers to utilize the BART model for summarization and sentiment analysis.
## Features
1. News Summarization: Provides a concise summary of news articles by extracting key information using NLP models.
2. Sentiment Analysis: Performs sentiment analysis on the content to determine the sentiment of the news (positive, neutral, negative).
3. User Interaction: Users can input news URLs, view summaries, and see sentiment analysis results directly through a web interface.

## Setup Instructions
1. Download all the files from the repository
2. Open command prompt and run the following command to install all the dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the application
   ```
   python manage.py runserver
   ```
   Visit the application in your web browser at http://127.0.0.1:8000/.
