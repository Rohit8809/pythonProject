
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Fetch News
def fetch_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    return news_data['articles']

# Prepare Full Articles
def prepare_full_articles(articles):
    full_articles = []
    for article in articles:
        description = article.get('description', 'No description available.')
        full_articles.append({'title': article['title'], 'description': description, 'link': article['url']})
    return full_articles

# Send Email
def send_email(articles, sender_email, sender_password, recipient_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Daily News Update"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    html = "<html><body>"
    html += "<h1>Daily News Update</h1>"
    for article in articles:
        html += f"<h3><a href='{article['link']}' target='_blank'>{article['title']}</a></h3><p>{article['description']}</p><hr>"
    html += "</body></html>"

    part = MIMEText(html, 'html')
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == "__main__":
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

    articles = fetch_news(NEWS_API_KEY)
    full_articles = prepare_full_articles(articles)
    send_email(full_articles, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)