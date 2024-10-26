import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from groq import Groq

# Replace with your actual Todoist API Key
API_KEY = 'a1c840bb12d5c6cef7bd9239dadb9b765d87855a'

# Initialize Groq client for Llama API
groq_client = Groq(
    api_key="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"
)

# Function to add a task in Todoist
def add_task(content, due_date=None, project_id=None):
    url = 'https://api.todoist.com/rest/v2/tasks'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Define the task data
    data = {'content': content}

    if due_date:
        data['due_date'] = due_date
    if project_id:
        data['project_id'] = project_id

    # Make the POST request to add the task
    response = requests.post(url, headers=headers, json=data)

    # Check the response status
    if response.status_code == 200 or response.status_code == 201:
        print("Task added successfully!")
        return response.json()
    else:
        print(f"Failed to add task: {response.status_code} - {response.text}")
        return None

# Summarize Tasks using Groq API
def summarize_task(content):
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following task: {content}"
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
        print(f"Error summarizing task: {str(e)}")
        return "Summary not available."

# Fetch tasks from Todoist and summarize them
def fetch_and_summarize_tasks(api_key):
    url = 'https://api.todoist.com/rest/v2/tasks'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        summarized_tasks = []
        for task in tasks:
            task_summary = summarize_task(task['content'])
            summarized_tasks.append({
                'content': task['content'],
                'summary': task_summary,
                'due': task.get('due', {}).get('date', 'No due date'),
                'url': task.get('url', '#')
            })
        return summarized_tasks
    else:
        print(f"HTTP error occurred: {response.status_code} - {response.text}")
        return []

# Send email with summarized tasks
def send_email(tasks, sender_email, sender_password, recipient_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Today’s Summarized To-Do List"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Construct HTML content for email with CSS styling
    html = """
    <html>
    <head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .task {
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .task h3 {
            margin: 0;
            font-size: 18px;
            color: #0056b3;
        }
        .task p {
            margin: 5px 0;
            color: #666;
        }
        .task a {
            color: #1a73e8;
            text-decoration: none;
        }
        .task a:hover {
            text-decoration: underline;
        }
        .footer {
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
        }
        .footer p {
            margin: 0;
        }
        .thank-you {
            font-family: 'Lora', serif;
            color: #FF5722;
            font-size: 22px;
            font-weight: bold;
        }
        .signature {
            font-family: 'Roboto', sans-serif;
            color: #4CAF50;
            font-size: 18px;
            font-weight: 500;
        }
    </style>
    </head>
    <body>
        <div class="container">
            <h1>Daily Summarized Task Digest</h1>
            <p style="font-family: Arial, sans-serif; font-size: 18px; color: #333; margin-bottom: 10px;">Hi Rohit</p>
            <h2 style="font-family: Arial, sans-serif; font-size: 24px; color: #0056b3; margin-bottom: 20px;">Today's Tasks and Summaries</h2>
    """

    if tasks:
        for task in tasks:
            html += f"""
            <div class='task'>
                <h3>{task['content']}</h3>
                <p>Summary: {task['summary']}</p>
                <p>Due: {task['due']}</p>
                <a href='{task['url']}'>View Task</a>
            </div>
            """
    else:
        html += "<p>No tasks found.</p>"

    html += """
        <div class="footer">
            <p class="thank-you">Thank You!</p>
            <p class="signature">Your Personal AI Productivity Manager</p>
        </div>
    </div>
    </body>
    </html>
    """

    part = MIMEText(html, 'html')
    msg.attach(part)

    # Send the email using SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")

if __name__ == "__main__":
    # Fetch environment variables for security (or replace with actual values)
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')  # Replace with your email
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'your_password')  # Replace with your email password
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'recipient_email@gmail.com')  # Replace with the recipient email

    # Add a sample task (optional)
    task_content = "Go to Bed for rest"
    due_date = "2024-09-08T03:05:00Z"  # Optional, in ISO 8601 format
    project_id = None  # Optional, provide a project ID if you want to add it to a specific project
    task = add_task(task_content, due_date, project_id)
    print(task)

    # Fetch and summarize tasks from Todoist
    tasks = fetch_and_summarize_tasks(API_KEY)

    # Check if tasks are fetched and summarized successfully
    if tasks:
        print(f"Fetched and summarized {len(tasks)} tasks.")
        send_email(tasks, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)
    else:
        print("No tasks found or an error occurred.")
