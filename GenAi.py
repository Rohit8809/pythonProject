from dotenv import load_dotenv
import openai
import os
import time

# Load environment variables from a .env file
load_dotenv()

# Fetch environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key is not set in the environment variables.")

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

# Example function to generate task descriptions
def generate_task_description(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Update to the model you are using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.RateLimitError as e:
        print(f"Rate limit error: {e}")
        print("Retrying after 60 seconds...")
        time.sleep(60)  # Wait before retrying
        return generate_task_description(prompt)  # Retry the request

# Example usage
prompt = "Generate a task description for a software development project."
task_description = generate_task_description(prompt)
print(task_description)
