import schedule
import time
import subprocess

# Define the task to run another Python script
def job():
    try:
        # Use subprocess to run the other Python script (e.g., news.py)
        subprocess.run(["python", "D:/Project/pythonProject/news.py"], check=True)
        print(f"news.py executed successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing news.py: {e}")

# Schedule the job to run every day at 2 AM
schedule.every(2).minutes.do(job)

# Continuously run the scheduler to check for pending tasks
while True:
    schedule.run_pending()  # Run all scheduled tasks that are pending
    time.sleep(60)  # Wait for 60 seconds before checking again
