from flask import Flask, render_template, jsonify
from newsAI import complete_articles
app = Flask(__name__)

# Sample news data
news_list = [
    {"title": "New AI technology breakthroughs", "description": "AI continues to revolutionize industries."},
    {"title": "Global markets continue to fluctuate", "description": "The stock market remains unpredictable."},
    {"title": "Scientists discover a new species", "description": "A rare new species found in the Amazon."},
    {"title": "Advances in renewable energy", "description": "Renewable energy solutions are on the rise."}
]

# API route to get news data
@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify(complete_articles)

# Route to serve the HTML UI
@app.route('/')
def index():
    return render_template('index.html')
# Initialize Groq client for Llama API
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

# Prepare Full Articles with Summarization and Images
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

if __name__ == '__main__':
    app.run(debug=False)

