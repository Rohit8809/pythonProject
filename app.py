from flask import Flask, render_template, jsonify
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from groq import Groq

app = Flask(__name__)


groq_client = Groq(
    api_key="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"
)


# Fetch News
def fetch_news(api_key, max_news=10):
    """
    Fetches the latest news articles using the Currents API.

    Parameters:
        api_key (str): The API key for accessing Currents API.
        max_news (int): Maximum number of news articles to fetch.

    Returns:
        list: A list of dictionaries containing news articles.
    """
    url = f'https://api.currentsapi.services/v1/latest-news?country=in&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        if 'news' in news_data:
            return news_data['news'][:max_news]  # Fetch only top 'max_news' articles
        else:
            print("Error: 'news' key not found in the response.")
            return []
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return []


# Summarize Articles using Groq API
def summarize_article(content):
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following article: {content}"
                }
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            stream=True,
            stop=None,
        )

        summary = ""
        for chunk in completion:
            summary += chunk.choices[0].delta.content or ""
        return summary
    except Exception as e:
        print(f"Error summarizing article: {str(e)}")
        return "Summary not available."


def prepare_full_articles(articles):
    """
    Prepares a list of full articles with titles, descriptions, and links.

    Parameters:
        articles (list): A list of articles to format.

    Returns:
        list: A list of formatted articles.
    """
    full_articles = []
    for article in articles:
        description = article.get('description', 'No description available.')
        summary = summarize_article(description)
        image_url = article.get('image', '')  # Fetch image URL if available
        full_articles.append({
            'title': article['title'],
            'description': summary,
            'link': article['url'],
            'image': image_url  # Include image URL
        })
    return full_articles


# API route to get news data
@app.route('/api/news', methods=['GET'])
def get_news():
    articles = fetch_news(NEWS_API_KEY, max_news=10)
    if not articles:
        print("No articles found or an error occurred.")
    else:
        print(f"Fetched {len(articles)} articles.")  # Debugging info
        full_articles = prepare_full_articles(articles)

    return jsonify(full_articles)


# Route to serve the HTML UI
@app.route('/')
def index():
    return render_template('index.html')


# Initialize Groq client for Llama API

if __name__ == "__main__":
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

    # Debugging info for environment variables
    print(f"NEWS_API_KEY: {NEWS_API_KEY}")
    print(f"SENDER_EMAIL: {SENDER_EMAIL}")
    print(f"SENDER_PASSWORD: {'***' if SENDER_PASSWORD else 'Not Set'}")
    print(f"RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")

    if not NEWS_API_KEY:
        print("Error: NEWS_API_KEY is not set.")
        exit(1)

    # Fetch only top 10 news articles
    articles = fetch_news(NEWS_API_KEY, max_news=10)
    if not articles:
        print("No articles found or an error occurred.")
    else:
        print(f"Fetched {len(articles)} articles.")  # Debugging info
        full_articles = prepare_full_articles(articles)

    app.run(debug=False)