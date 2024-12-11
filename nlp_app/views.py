from django.shortcuts import render
from newspaper import Article
from transformers import BartTokenizer, pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re

# Download necessary data
nltk.download("vader_lexicon")

# Initialize NLP models
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")
sia = SentimentIntensityAnalyzer()

# Function to clean text
def clean_text(text):
    """Clean the input text by removing extra spaces, special characters, and unnecessary formatting."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'\[.*?\]', '', text)  # Remove text within brackets
    text = re.sub(r'[^a-zA-Z0-9.,\s]', '', text)  # Remove special characters except punctuation
    text = text.strip()  # Remove leading/trailing spaces
    return text

# Function for text summarization
def summarize_text(text):
    try:
        # Summarize using BART
        summary = summarizer(
            text,
            max_length=200,  
            min_length=80,
            do_sample=True,  
        )
        return summary[0]["summary_text"]
    except Exception as e:
        return f"Error in summarization: {e}"

def home(request):
    context = {}
    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            try:
                # Extract article
                article = Article(url)
                article.download()
                article.parse()
                article_text = article.text

                # Clean the article text
                cleaned_text = clean_text(article_text)

                # Summarize the cleaned text
                summary_text = summarize_text(cleaned_text)

                # Sentiment Analysis
                sentiment = sia.polarity_scores(summary_text)
                overall_sentiment = (
                    "Positive" if sentiment["compound"] >= 0.05
                    else "Negative" if sentiment["compound"] <= -0.05
                    else "Neutral"
                )

                # Pass data to the results page
                context = {
                    "article_text": cleaned_text,
                    "summary": summary_text,
                    "sentiment": {
                        "positive": sentiment["pos"],
                        "neutral": sentiment["neu"],
                        "negative": sentiment["neg"],
                        "compound": sentiment["compound"],
                    },
                    "overall_sentiment": overall_sentiment,
                }

            except Exception as e:
                context["error"] = f"An error occurred: {e}"
    return render(request, "index.html", context)

