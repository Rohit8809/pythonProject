import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Fetch Tasks
def fetch_tasks(api_key):
    url = 'https://api.todoist.com/rest/v2/projects'  # Ensure this is the correct URL
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()
    # Check if the response status is OK
    # if response.status_code == 200:
    #     return response.json()
    # elif response.status_code == 410:
    #     print("Error 410: The requested resource is no longer available.")
    #     return []
    # else:
    #     response.raise_for_status()  # Raise an error for other HTTP status codes

# Send Email
def send_email(projects, sender_email, sender_password, recipient_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Todoist Projects"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    html = "<html><body>"
    html += "<h1>Your Task Management</h1>"
    for project in projects:
        project_link = f'<a href="{project["url"]}">{project["name"]}</a>'
        html += f"<h3>{project_link}</h3><p>Comments: {project['comment_count']}</p><p>Color: {project['color']}</p><hr>"
    html += "</body></html>"

    part = MIMEText(html, 'html')
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == "__main__":
    TODOIST_API_KEY = os.getenv('TODOIST_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

    tasks = fetch_tasks(TODOIST_API_KEY)
    if tasks:  # Proceed only if tasks are successfully fetched
        send_email(tasks, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)