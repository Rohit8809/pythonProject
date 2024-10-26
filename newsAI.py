import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from groq import Groq

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
complete_articles=prepare_full_articles(articles)

# Send Email with News and Photos
def send_email(articles, sender_email, sender_password, recipient_email):
    """
    Sends an email containing the list of articles in an HTML formatted body.

    Parameters:
        articles (list): A list of articles to include in the email.
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_email (str): Recipient's email address.
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Today’s Headlines: Fresh Updates Await"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Email HTML template
    html_template = """
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 90%;
                max-width: 900px;
                margin: 20px auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 32px;
                margin-bottom: 20px;
                text-align: center;
            }}
            h3 {{
                color: #007BFF;
                font-size: 24px;
                margin: 15px 0 5px;
            }}
            p {{
                color: #555;
                font-size: 16px;
                line-height: 1.6;
                margin: 10px 0;
            }}
            a {{
                color: #007BFF;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            img {{
                max-width: 100%;
                height: auto;
                margin: 10px 0;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            hr {{
                border: 0;
                border-top: 1px solid #eee;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 15px;
                border-top: 1px solid #ddd;
                text-align: center;
            }}
            .footer p {{
                margin: 5px 0;
                color: #777;
            }}
            .thank-you {{
                color: #FF5722;
                font-size: 20px;
                font-weight: bold;
            }}
            .signature {{
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>News at a Glance: What’s Happening Today</h1>
           <p style="font-family: Arial, sans-serif; font-size: 18px; color: #333; margin-bottom: 10px;">Hi Rohit</p>
            <h2 style="font-family: Arial, sans-serif; font-size: 24px; color: #0056b3; margin-bottom: 20px;">Breaking News: What You Need to Know</h2>

            {articles}
            <div class="footer">
                <p class="thank-you" style="font-family: 'Lora', serif; color: #FF5722; font-size: 22px; font-weight: bold;">Thank You!</p>
                <p class="signature" style="font-family: 'Roboto', sans-serif; color: #4CAF50; font-size: 18px; font-weight: 500;">Your Personal AI Productivity Manager</p>
            </div>
        </div>
    </body>
    </html>
    """

    articles_html = ""
    for article in articles:
        image_html = f"<img src='{article['image']}' alt='News Image'>" if article['image'] else ""
        articles_html += f"""
        <h3><a href='{article['link']}' target='_blank'>{article['title']}</a></h3>
        {image_html}
        <p>{article['description']}</p>
        <hr>
        """

    html_content = html_template.format(articles=articles_html)

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")

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
        send_email(full_articles, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)
